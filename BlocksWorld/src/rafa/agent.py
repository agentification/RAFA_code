import re
import torch
import numpy as np
from copy import deepcopy
from typing import List, Tuple
from src.models import QueryLM
from src.rafa.tree_search import TreeSearch, AbsNode
from src.utils.blocksworld import apply_change, generate_all_actions, get_world_change, extract_block, count_obstacles
from src.rafa.utils import llm_count_obstacles


class StateNode(AbsNode):
    def __init__(self, prompt, rwd_fn, v_fn, alpha, depth, max_depth, parent=None, prob_r=0):
        self.children = []
        self.depth = depth # real depth, not relative depth
        self.max_depth = max_depth
        self.parent = parent
        self._alpha = alpha
        self.rwd_fn = rwd_fn
        self.v_fn = v_fn
        self._prob_r = prob_r
        self.prompt, self._v_rand = v_fn(prompt, depth)

    def _create_child_node(self, prompt, prob_r):
        return StateNode(prompt, self.rwd_fn, self.v_fn, self._alpha, self.depth + 1, self.max_depth, parent=self, prob_r=prob_r)

    def _get_children(self):
        if self.is_terminal:
            return self.children
        questions, arr_prob_r = self.rwd_fn(self.prompt, self.depth)
        self.actions = questions
        for question, prob_r in zip(questions, arr_prob_r):
            child = self._create_child_node(question, prob_r)
            if child.achieved_goal: # be careful of this
                return [child]
            self.children.append(child)
        return self.children

    def get_children(self):
        self.children = self.children or self._get_children()
        return self.children

    @property
    def achieved_goal(self) -> bool:
        return self._v_rand >= 1e3

    @property
    def is_terminal(self) -> bool:
        return self.depth > self.max_depth or self.achieved_goal


def forward_plan(initial_state: str,
                 goal: str,
                 prompts: dict,
                 world_model: QueryLM,
                 alpha: float,
                 n_trials: int,
                 horizon: int,
                 search_depth: int,
                 sample_per_node: int,
                 sampler: str='heuristic',
                 discount: float=1,
                 speedup_action_batch_size=2,
                 use_lang_goal=False,
                 use_mem_prompt=False) -> bool:

    subgoal_memory = ""

    '''-----------------------------------------------------'''

    def rwd_fn(inp, depth) -> Tuple[List, np.ndarray]:
        '''For r=Pr(a|s_t), the probability component reward'''
        # extract the last state
        last_state = re.search(f'.*{re.escape(prompts["state_prefix"].format(depth))}(.*)', inp)[1]
        # pure action description without some prefix like '[ACTION n]'
        raw_action_list = generate_all_actions(last_state)
        # calculate action index
        n_base_actions = 2 * (depth // 2)
        # add prefix for actions
        action_output = [inp + prompts["action_prefix"].format(depth + 1) + " " + a.capitalize() + ".\n" for a in raw_action_list]
        last_base_state = inp.split(prompts["state_prefix"].format(n_base_actions))[-1].split(prompts["action_prefix"].format(n_base_actions + 1))[0].strip()
        baseline_prompt = prompts["baseline_action"]
        baseline_prompt += "\n[STATEMENT]\n"
        baseline_prompt += "As initial conditions " + last_base_state.strip() + "\n" + inp.split("[GOAL]")[-1].split("[STATE 0]")[0].strip() + "\n\nMy plan is as follows:\n\n[PLAN]\n"
        action_list = []
        lastest_list = []
        new_action_output = []
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
        scores = np.array(scores)
        exp_scores = np.exp(scores)
        soft_scores = exp_scores / np.sum(exp_scores)
        return new_action_output, soft_scores

    '''-----------------------------------------------------'''

    def v_fn(inp, depth) -> Tuple[str, float]:

        nonlocal subgoal_memory

        if depth == 0:
            return inp, 0
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
        world_output = world_model.query_LM(world_update_prompt)
        # world_change = get_world_change(last_state, last_action)
        world_change = world_output.split("[CHANGE]")[-1]
        last_state = inp.split(f"[STATE {depth-1}]")[-1].split(f"[ACTION {depth}]")[0]
        new_state = apply_change(world_change, last_state)
        new_prompt = inp + prompts["state_prefix"].format(depth) + " " + new_state + "\n"
        # method 1: simple goal alignment
        # goal_statement = inp.split("[GOAL]")[-1].split("[STATE 0]")[0]
        # goals = re.findall("the [a-z]{0,10} block is on top of the [a-z]{0,10} block", goal_statement)
        # meetings = [g in new_state for g in goals]
        # v = 200 if sum(meetings) == len(meetings)\
        #     else sum(meetings) / len(meetings) + 0.5
        # method 2: 
        goal_statement = inp.split("[GOAL]")[-1].split("[STATE 0]")[0]
        final_goals = re.findall("the [a-z]{0,10} block is on top of the [a-z]{0,10} block", goal_statement)
        meetings = [g in new_state for g in final_goals]
        if sum(meetings) == len(meetings):
            return new_prompt, 1e3
        goal_alignment = 0
        print('the new state is:', new_state)
        print('counting goals...')
        for fg in final_goals:
            print('current fg=', fg)
            if fg in new_state:
                print('final goal aligned++')
                goal_alignment += 1
                continue
            topper = extract_block(
                fg.split("top of")[0]
            )
            bottomer = extract_block(
                fg.split("top of")[1]
            )
            print('topper', topper)
            print('bottomer', bottomer)
            if bottomer + " is clear" in new_state and 'holding ' + topper in new_state:
                print('doorway goal++')
                goal_alignment += 0.5
                continue
            if use_lang_goal != True:
                tmp = count_obstacles(topper, new_state)
                print('true topper obstacles', tmp)
                goal_alignment -= tmp
                tmp = count_obstacles(bottomer, new_state)
                print('true bottomer obstacles', tmp)
                goal_alignment -= tmp
            else:
                tmp = llm_count_obstacles(topper, new_state, world_model, subgoal_memory)
                print('lang topper obstacles', tmp)
                goal_alignment -= tmp
                tmp = llm_count_obstacles(bottomer, new_state, world_model, subgoal_memory)
                print('lang bottomer obstacles', tmp)
                goal_alignment -= tmp
        print('vrand=', goal_alignment)
        return new_prompt, goal_alignment

    '''-----------------------------------------------------'''

    def calc_real_reward(node):

        nonlocal subgoal_memory

        goal_statement = node.prompt.split("[GOAL]")[-1].split("[STATE 0]")[0]
        final_goals = re.findall("the [a-z]{0,10} block is on top of the [a-z]{0,10} block", goal_statement)
        new_state = re.search(f'.*{re.escape(prompts["state_prefix"].format(node.depth - 1))}(.*)', node.prompt)[1]
        meetings = [g in new_state for g in final_goals]
        if sum(meetings) == len(meetings):
            return 1e3
        goal_alignment = 0
        for fg in final_goals:
            print('current fg=', fg)
            if fg in new_state:
                print('final goal aligned++')
                goal_alignment += 1
                continue
            topper = extract_block(
                fg.split("top of")[0]
            )
            bottomer = extract_block(
                fg.split("top of")[1]
            )
            print('topper', topper)
            print('bottomer', bottomer)
            if bottomer + " is clear" in new_state and 'holding ' + topper in new_state:
                print('doorway goal++')
                goal_alignment += 0.5
                continue
            tmp = count_obstacles(topper, new_state)
            print('true topper obstacles', tmp)
            goal_alignment -= tmp
            # update memory for topper
            if use_mem_prompt:
                new_state = re.search(f'.*{re.escape(prompts["state_prefix"].format(cur_node.depth - 1))}(.*)', cur_node.prompt)[1]
                subgoal_memory += "[STATE]{}\nQuestion:how many blocks are piled on {}?\n[STATE STATUS]{}\n".format(new_state, topper, tmp)
            tmp = count_obstacles(bottomer, new_state)
            print('true bottomer obstacles', tmp)
            goal_alignment -= tmp
            # update memory for bottomer
            if use_mem_prompt:
                new_state = re.search(f'.*{re.escape(prompts["state_prefix"].format(cur_node.depth - 1))}(.*)', cur_node.prompt)[1]
                subgoal_memory += "[STATE]{}\nQuestion:how many blocks are piled on {}?\n[STATE STATUS]{}\n".format(new_state, bottomer, tmp)
        return goal_alignment

    '''-----------------------------------------------------'''

    planner = TreeSearch(
        search_depth=search_depth,
        sample_per_node=sample_per_node,
        sampler=sampler,
        discount=discount
    )
    pmpt_list = []
    cur_node = StateNode(
        prompt=prompts["goal_prefix"] + goal.strip() + "\n" + prompts["state_prefix"].format(0) + " " + initial_state.strip() + "\n",
        rwd_fn=rwd_fn,
        v_fn=v_fn,
        alpha=alpha,
        depth=0,
        max_depth=horizon
    )
    for i in range(n_trials):
        while not cur_node.is_terminal:
            cur_node = planner(cur_node)
            # update critic
            cur_node._v_rand = calc_real_reward(cur_node)
        pmpt_list.append(cur_node.prompt)
        if cur_node.achieved_goal:
            return i, pmpt_list
    return -1, pmpt_list