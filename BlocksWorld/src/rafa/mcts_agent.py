import io
import json
import os
import random
import re
import sys
import traceback
import warnings
from collections import defaultdict
from typing import Tuple
from copy import deepcopy
import torch
from src.utils.blocksworld import apply_change, generate_all_actions, get_world_change

from src.rafa.mcts import MCTS, MCTSNode
from src.models import QueryLM
from tqdm import tqdm, trange
import numpy as np

class ReasoningMCTSNode(MCTSNode):
    @property
    def visited(self):
        return self._visited

    def __init__(self, prompt, gen_fn, reward_fn, depth, r1_default, r_alpha, max_depth=100, parent: 'ReasoningMCTSNode' = None, r0=0., ):
        self._conf = None
        self.children = []
        self.prompt = prompt
        self.gen_fn = gen_fn
        self.reward_fn = reward_fn
        self.depth = depth
        self._r0 = r0
        self._r1 = self._r1_default = r1_default
        self._r_alpha = r_alpha
        self._ans_list = None
        self._visited = False
        self.parent = parent
        self.max_depth = max_depth
        self.questions = None
        self.children_question_map = None

    def _child_node(self, prompt, r0):
        return ReasoningMCTSNode(prompt, self.gen_fn, self.reward_fn, self.depth + 1, self._r1_default, self._r_alpha, parent=self, r0=r0, max_depth=self.max_depth)

    def _get_children(self):
        self._visited = True
        self._calculate_reward()
        if self.is_terminal:
            return self.children
        self.questions, r0 = self.gen_fn(self.prompt, self.depth)
        for question, r in zip(self.questions, r0):
            self.children.append(self._child_node(question, r))
        # map action and children
        self.children_question_map = dict()
        for i, child in enumerate(self.children):
            self.children_question_map[child] = self.questions[i]
        return self.children

    def child_to_question(self, child):
        if child not in self.children_question_map.keys():
            raise KeyError
        return self.children_question_map[child]

    def find_children(self):
        self.children = self.children or self._get_children()
        return self.children

    def find_one_child(self) -> MCTSNode:
        return random.choice(self.find_children())

    def _calculate_reward(self):
        # NOTE: temporary
        if self.depth == 0:
            return
        self.prompt, self._r1, self._ans_list = self.reward_fn(self.prompt, self.depth)

    def _static_terminal(self):
        if self._r1 > 50:
            return True
        elif self.depth >= self.max_depth:
            return True
        else:
            return False


    @property
    def is_terminal(self):
        return self._static_terminal() or self.reward < -1

    @property
    def reward(self):
        if self._r0 < 0 or self._r1 < 0:
            return min(self._r0, self._r1)
        
        return self._r0 ** self._r_alpha * self._r1 ** (1 - self._r_alpha)

    def print(self, mcts: MCTS, file=None):
        def pprint(*args):
            if file is None:
                pass
            else:
                print(*args, file=file)
        p1 = '-' * (4 * self.depth - 4)
        prefix = ' ' * (4 * self.depth - 4)
        question = self.prompt.split("[PLAN]\n")[-1].replace("\n", "\\n")
        pprint(p1 + question)
        pprint(prefix + f'R: {self.reward:.3f} ; N: {mcts.N[self]} ; M: {mcts.M[self]:.3f} ; r0 : {self._r0:.3f}')
        if not self.visited:
            return
        if self.reward < -1:
            if file is not None:
                pprint(prefix + question)
            return
        
        for child in self.children:
            child.print(mcts, file)
        if self.depth == 1:
            pprint("=" * 12)

    def __setstate__(self, state):
        self.__dict__.update(state)
        if self.gen_fn is None or self.reward_fn is None:
            warnings.warn('MCTSNode loaded from pickle is read-only; Do not further roll out the tree!')

    def __getstate__(self):
        state = self.__dict__.copy()
        state['gen_fn'] = None
        state['reward_fn'] = None
        return state


def reasoning_mcts_search(initial_state: str,
                          goal: str,
                          prompts,
                          world_model: QueryLM,
                          temperature,
                          mcts_steps,
                          n_sample_confidence,
                          max_depth,
                          r_alpha,
                          r1_default,
                          eos_token_id,
                          speedup_action_batch_size=2,
                          w_exp=1):

    def gen_fn(inp, depth):
        last_state = re.search(f'.*{re.escape(prompts["state_prefix"].format(depth))}(.*)', inp)[1]

        raw_action_list = generate_all_actions(last_state)
        action_output = [inp + prompts["action_prefix"].format(depth + 1) + " " + a.capitalize() + ".\n" for a in raw_action_list]
        new_action_output = []
        n_base_actions = 2 * (depth // 2)
        if world_model.__class__.__name__ == 'QueryChatGPT':
            scores = world_model.smp_get_ll(inp + ("[ACTION {}]".format(n_base_actions + 1)), raw_action_list)
            exp_scores = np.exp(scores)
            soft_scores = exp_scores / np.sum(exp_scores)
            return action_output, soft_scores
        last_base_state = inp.split(prompts["state_prefix"].format(n_base_actions))[-1].split(prompts["action_prefix"].format(n_base_actions + 1))[0].strip()
        baseline_prompt = prompts["baseline_action"]
        baseline_prompt += "\n[STATEMENT]\n"
        baseline_prompt += "As initial conditions " + last_base_state.strip() + "\n" + inp.split("[GOAL]")[-1].split("[STATE 0]")[0].strip() + "\n\nMy plan is as follows:\n\n[PLAN]\n"

        action_list = []
        lastest_list = []
        for a in action_output:
            history = "".join(re.findall(r'\[ACTION \d+\] .*?\n', a)).replace(".", "")
            identifier = re.findall("\[ACTION \d+\]", history)
            for id in identifier:
                history = history.replace(id, "")
            history = history.strip().replace("\n ", "\n")
            torch.distributed.barrier()
            new_action_output.append(a)
            action_list.append(history)
            lastest_list.append("\n".join(history.split("\n")[-1 if depth % 2 == 0 else -2:]))

        ll_prompts = [baseline_prompt + a.lower() for a in lastest_list]
        
        scores = []
        for idx in range(0, len(ll_prompts), speedup_action_batch_size):
            end_idx = min(idx + speedup_action_batch_size, len(ll_prompts))
            if world_model.__class__.__name__ == 'QueryVicuna':
                log_probs = world_model.get_ll(baseline_prompt, ll_prompts[idx: end_idx])
            else:
                log_probs = world_model.llamamodel.get_ll(baseline_prompt, ll_prompts[idx: end_idx])
            scores += list(log_probs)

        # softmax scores
        scores = np.array(scores)
        exp_scores = np.exp(scores)
        soft_scores = exp_scores / np.sum(exp_scores)
        
        for a, s in zip(new_action_output, soft_scores):
            history = "".join(re.findall(r'\[ACTION \d+\].*?\n', a)).replace(".", "")
            identifier = re.findall("\[ACTION \d+\]", history)
            for id in identifier:
                history = history.replace(id, "")
            history = history.strip()

        return new_action_output, soft_scores
    
    def r1_fn(inp, depth):

        if depth == 0:
            return 1.0, inp, []
        
        last_state = re.search(f'.*{re.escape(prompts["state_prefix"].format(depth - 1))}(.*)', inp)[1]
        last_action = re.search(f'.*{re.escape(prompts["action_prefix"].format(depth))}(.*)', inp)[1]

        if "Pick" in last_action: 
            world_update_prompt = prompts["world_update_pickup"].format(last_state, last_action)
        elif "Unstack" in last_action:
            world_update_prompt = prompts["world_update_unstack"].format(last_state, last_action)
        elif "Put" in last_action:
            world_update_prompt = prompts["world_update_putdown"].format(last_state, last_action)
        elif "Stack" in last_action: 
            world_update_prompt = prompts["world_update_stack"].format(last_state, last_action)

        if world_model.__class__.__name__ == "QueryVicuna":
            world_output = world_model.query_LM(world_update_prompt)
        else:
            world_output = world_model.query_LM(world_update_prompt, do_sample=False, num_return_sequences=1,
                                        eos_token_id=eos_token_id)[0]
        world_change = world_output.split("[CHANGE]")[-1]
        last_state = inp.split(f"[STATE {depth-1}]")[-1].split(f"[ACTION {depth}]")[0]
        new_state = apply_change(world_change, last_state)
        new_prompt = inp + prompts["state_prefix"].format(depth) + " " + new_state + "\n"
        goal_statement = inp.split("[GOAL]")[-1].split("[STATE 0]")[0]
        goals = re.findall("the [a-z]{0,10} block is on top of the [a-z]{0,10} block", goal_statement)
        meetings = [g in new_state for g in goals]
        if sum(meetings) == len(meetings):
            r1 = 100
        else:
            r1 = sum(meetings) / len(meetings) + 0.5
        return r1, new_prompt, []

    def reward_fn(inp, depth):
        r1, answer, ans_list = r1_fn(inp, depth)
        return answer, r1, ans_list

    def true_dynamics(inp: str, depth: int) -> Tuple[float, str]:
        last_state = re.search(f'.*{re.escape(prompts["state_prefix"].format(depth - 1))}(.*)', inp)[1]
        last_action = re.search(f'.*{re.escape(prompts["action_prefix"].format(depth))}(.*)', inp)[1]
        world_change = get_world_change(last_state, last_action)
        new_state = apply_change(world_change, last_state)
        new_prompt = inp + prompts["state_prefix"].format(depth) + " " + new_state + "\n"
        goal_statement = inp.split("[GOAL]")[-1].split("[STATE 0]")[0]
        goals = re.findall("the [a-z]{0,10} block is on top of the [a-z]{0,10} block", goal_statement)
        meetings = [g in new_state for g in goals]
        if sum(meetings) == len(meetings):
            r1 = 100
        else:
            r1 = sum(meetings) / len(meetings) + 0.5
        return r1, new_prompt

    mcts = MCTS(w_exp=w_exp, prior=True, aggr_reward='mean', aggr_child='max')
    root = ReasoningMCTSNode(prompts["goal_prefix"] + goal.strip() + "\n" + prompts["state_prefix"].format(0) + " " + initial_state.strip() + "\n", gen_fn, reward_fn, depth=0, r1_default=r1_default, r_alpha=r_alpha, max_depth=max_depth)
    trajs = []
    trees = []
    for _ in (pbar := trange(mcts_steps, disable=bool(int(os.environ.get("LOCAL_RANK", -1))), position=0)):
        node = root
        while not node.is_terminal:
            # print('node', node.prompt)
            path = mcts.rollout(node)
            max_n, max_r = mcts.max_mean_terminal(root) # max-end-node, max-return
            # print('max_n', max_n.prompt)

            next_node = max_n
            while next_node.parent != node: next_node = next_node.parent # find the next-node
            # print('next_node', next_node.prompt)

            next_question = node.child_to_question(next_node) # find the corresponding next-question (world change question)
            next_node._r1, next_node.prompt = true_dynamics(next_question, next_node.depth) # receive real env feedback

            node = next_node # materialize real transition

            mcts.memory_propagate(path) # update value estimation with env feedback
        trajs.append(traj := node.prompt)
        output = re.findall('The answer is .*?([.0-9,\\-]+).*\\.', traj)
        if len(output) == 0:
            temp_r = 'not found'
        else:
            temp_r = output[-1].replace(',', '')
        pbar.set_description(f'{max_r:.3f} {temp_r}')
        tree_copy = deepcopy(root)
        tree_copy.Q = dict(mcts.Q)
        tree_copy.N = dict(mcts.N)
        tree_copy.M = dict(mcts.M)
        trees.append(tree_copy)

    with io.StringIO() as f:
        root.print(mcts, file=f)
        tree = f.getvalue()
    return trajs, tree, trees