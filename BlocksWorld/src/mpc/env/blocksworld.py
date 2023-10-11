import os
os.environ['OPENAI_API_KEY'] = '0'
import re
import json
import numpy as np
from copy import deepcopy
from tarski.io import PDDLReader
from collections import OrderedDict
from typing import List, Dict, Tuple
import colorama
from colorama import Fore
from colorama import Style
colorama.init()


with open('data/blocksworld/spells.json') as f:
    SPELLS = json.load(f)


def get_problem(instance, domain):
    reader = PDDLReader(raise_on_error=True)
    reader.parse_domain(domain)
    return reader.parse_instance(instance)


def generate_all_actions(state: str) -> List[str]:
    return_list = []
    if "hand is empty" in state:
        block = re.findall("the [a-z]{0,10} block is clear", state)
        block_color = [re.search("the ([a-z]{0,10}) block is clear", b).group(1) for b in block]
        for c in block_color:
            if f"the {c} block is on the table" in state:
                return_list.append(f"Pick up the {c} block")
            else:
                c_ = re.search(f"the {c} block" + " is on top of the ([a-z]{0,10}) block", state).group(1)
                return_list.append(f"Unstack the {c} block from on top of the {c_} block")
    else:
        c = re.search("is holding the ([a-z]{0,10}) block", state).group(1)
        block = re.findall("the [a-z]{0,10} block is clear", state)
        clear_color = [re.search("the ([a-z]{0,10}) block is clear", b).group(1) for b in block]
        for c_ in clear_color:
            return_list.append(f"Stack the {c} block on top of the {c_} block")
        return_list.append(f"Put down the {c} block")
    return return_list


def apply_change(change, state):
    if "and the " in state and ", and the" not in state:
        state = state.replace("and the ", ", and the ")
    states = state.split(", ")
    states = [s.strip()[4:].strip(".") if s.strip().startswith("and ") else s.strip().strip(".") for s in states]
    changes = change.lower().strip().strip(".").split(", ")
    for c in changes:
        if c.startswith("and "):
            c = c[4:]
        success = 0
        if c.startswith("the hand"):
            old = c.split("was")[1].split("and")[0].strip()
            new = c.split("now")[1].strip()
            for idx in range(len(states)):
                if ("hand is " + old) in states[idx]:
                    states[idx] = states[idx].replace(old, new)
                    success += 1
        else:
            
            colors = re.findall(r"the (\w+) block", c)
            if len(colors) == 0:
                print("Error: zero-colors")
                print(c)
                raise Exception("ERROR")
            color = colors[0]
            # print(colors)
            if c.startswith(f"the {color} block"):
                # print("SUB:", f"the {color} block")
                subj = f"{color} block"
                if "no longer" in c:
                    old = c.split("no longer")[1].strip()
                    # print("old:", old)
                    for idx in range(len(states)):
                        if f"{color} block is " + old in states[idx]:
                            states[idx] = ""
                            success += 1
                elif "was" in c and "now" in c:
                    old = c.split("was")[1].split(" and")[0].strip()
                    new = c.split("now")[1].strip()
                    # print("previous:", "{color} block is " + old)
                    for idx in range(len(states)):
                        if f"{color} block is " + old in states[idx]:
                            states[idx] = states[idx].replace(old, new)
                            success += 1
                elif "now" in c:
                    new = c.split("now")[1].strip()
                    states.append("the " + color + " block is " + new)
                    success += 1
            else:
                # print("ERROR")
                print("Error: not recognized")
                raise Exception("ERROR")
        if success == 0:
            # print("ERROR")
            print("Error: no successful change")
            print(c)
            print(states)
            raise Exception("ERROR")
        # print("current states:", states)
    states = [s for s in states if s != ""]
    priority_states = []
    for s in states:
        if "have that" in s:
            priority_states.append(0)
        elif "clear" in s:
            priority_states.append(1)
        elif "in the hand" in s:
            priority_states.append(1)
        elif "the hand is" in s:
            priority_states.append(2)
        elif "on top of" in s:
            priority_states.append(3)
        elif "on the table" in s:
            priority_states.append(4)
        else:
            print("Error: unknown state")
            print(s)
            raise Exception("ERROR")
    sorted_states = [x.strip() for _, x in sorted(zip(priority_states, states))]
    sorted_states[-1] = "and " + sorted_states[-1]
    return ", ".join(sorted_states) + "."


def get_world_change(last_state, last_action):

    '''  solve the hand state. note that the sentence could end with "." or ","  '''
    hand_pattern = r"(the hand is .*?[,\.])"
    # find the last description of hand status
    hand_last_state = re.findall(hand_pattern, last_state)[0][:-1]
    # replace "is" with "was" for the world_change format
    hand_last_state_past_tense = hand_last_state.replace('is', 'was')
    # turn the string into a list to change "the" to "The"
    hand_last_state_past_tense = list(hand_last_state_past_tense)
    hand_last_state_past_tense[0] = 'T'
    hand_last_state_past_tense = "".join(hand_last_state_past_tense)

    '''  solve the manipulated block state. note that the sentence could end with "." or ","  '''
    block_info_index1 = last_action.index('the')
    block_info_index2 = last_action.index('block')
    block_info = last_action[block_info_index1:block_info_index2+6]
    # remove the ending spaces and '.'
    block_info = block_info.replace('.', '')
    block_info = block_info.rstrip()
    block_pattern = r"(" + block_info + r" is .*?[,\.])"
    block_last_state = re.findall(block_pattern, last_state)[0][:-1]
    # replace "is" with "was" for the world_change format
    block_last_state_past_tense = block_last_state.replace('is', 'was')

    if "Pick" in last_action: 
        hand_change = hand_last_state_past_tense + ' and is now holding ' + block_info
        block_change = block_info + ' was on the table and is now in the hand'
        table_change = 'and ' + block_info + ' is no longer clear'
    elif "Unstack" in last_action:
        hand_change = hand_last_state_past_tense + ' and is now holding ' + block_info
        '''  solve the table related state'''
        holder_info_index1 = last_action.index('on top of the ')
        holder_info = last_action[holder_info_index1+10:]
        holder_info_index2 = holder_info.index('block')
        holder_info = holder_info[:holder_info_index2+6]
        # remove the ending spaces and '.'
        holder_info = holder_info.replace('.', '')
        holder_info = holder_info.rstrip()
        block_change = block_info + ' was on top of ' + holder_info + ' and is now in the hand, ' + block_info + ' is no longer clear'
        table_change = holder_info + ' is now clear'
    elif "Put" in last_action:
        hand_change = hand_last_state_past_tense + ' and is now empty'
        block_change = block_last_state_past_tense + ' and is now on the table'
        table_change = 'and ' + block_info + ' is now clear'
    elif "Stack" in last_action: 
        hand_change = hand_last_state_past_tense + ' and is now empty'
        '''  solve the table related state'''
        holder_info_index1 = last_action.index('on top of the ')
        holder_info = last_action[holder_info_index1+10:]
        holder_info_index2 = holder_info.index('block')
        holder_info = holder_info[:holder_info_index2+6]
        # remove the ending spaces and '.'
        holder_info = holder_info.replace('.', '')
        holder_info = holder_info.rstrip()
        block_change = block_last_state_past_tense + ' and is now on top of ' + holder_info + ', ' + holder_info + ' is no longer clear'
        table_change = 'and ' + block_info + ' is now clear'

    return hand_change + ', ' + block_change + ', ' + table_change + '.'


class StateNode:
    def __init__(self, goal_statement: str, father: "StateNode", depth: int, max_depth: int, root_path: List[str], self_state: str) -> None:
        self.est_goal = 0
        self.goal_statement = goal_statement
        self.goals = re.findall("the [a-z]{0,10} block is on top of the [a-z]{0,10} block", goal_statement)
        self.future_tense = [goal.replace('is', 'to be') for goal in self.goals]
        self.completed_subgoals = sum([g in self_state for g in self.goals])
        self.total_subgoals = len(self.goals)
        self.depth = depth
        self.max_depth = max_depth
        self.father = father
        self.self_state = self_state
        self._children = None
        self.action_space = None
        self._action_index = None
        self.root_path = root_path
        self.root_path.append('[state {}] '.format(depth)+self_state)
        self.root_path.append('[total subgoals] '+str(self.total_subgoals))
        self.root_path.append('[completed subgoals] '+str(self.completed_subgoals))
        self.v = 0
        self.r = OrderedDict()
        self.q = OrderedDict()

    @property
    def is_leaf(self) -> bool:
        return self.depth >= self.max_depth

    @property
    def children(self) -> None or List["StateNode"]:
        self.generate_children()
        return self._children

    @property
    def action_index(self) -> None or OrderedDict:
        self.generate_children()
        return self._action_index

    def find_action(self, child: "StateNode") -> str:
        ind = self._children.index(child)
        assert self.action_space is not None
        return self.action_space[ind]

    def find_child(self, action: str) -> "StateNode":
        self.generate_children()
        return self._children[self._action_index[action]]

    def generate_children(self) -> None:
        if self._children is not None or self.is_leaf:
            return
        self._children = []
        self.action_space = generate_all_actions(self.self_state)
        self._action_index = OrderedDict()
        for ind, action in enumerate(self.action_space):
            self._action_index[action] = ind
            world_change = get_world_change(
                last_state=self.self_state,
                last_action=action,
            )
            new_state = apply_change(
                change=world_change,
                state=self.self_state,
            )
            new_path = deepcopy(self.root_path)
            new_path.append('[action {}] '.format(self.depth+1)+action)
            self._children.append(
                StateNode(goal_statement=self.goal_statement,
                          father=self,
                          depth=self.depth+1,
                          max_depth=self.max_depth,
                          root_path=new_path,
                          self_state=new_state
                )
            )

    def to_dict(self) -> Dict:
        '''Convert the subtree recursively to a dict'''
        d = {
            "depth": self.depth,
            "self_state": self.self_state,
            "action_space": self.action_space,
            "v": self.v,
            "r": self.r,
            "q": self.q,
        }
        if self.father is None:
            d["goal_statement"] = self.goal_statement
            d["max_depth"] = self.max_depth
        if self._children is not None:
            d["children"] = [child.to_dict() for child in self._children]
        return d


class Blocksworld:
    def __init__(self,
                 max_steps: int,
                 alpha_1: float,
                 alpha_2: float,
                 initial_state: str,
                 goal_statement: str) -> None:
        self.root = StateNode(
            goal_statement=goal_statement,
            father=None, depth=0, max_depth=max_steps,
            root_path=[],
            self_state=initial_state
        )
        self.cur_node = self.root
        self.max_steps = max_steps
        self.alpha_1 = alpha_1 # the learning rate for prob values
        self.alpha_2 = alpha_2 # the learning rate for subgoal values
        self.initial_state = initial_state
        self.goal_statement = goal_statement
        self.goals = re.findall("the [a-z]{0,10} block is on top of the [a-z]{0,10} block", goal_statement)
        self.future_tense = [goal.replace('is', 'to be') for goal in self.goals]
        self.history = []
        self.action_history = []
        self.action_option_history = []
        self.cur_step = 0

    def get_action_space(self, state: str) -> List[str]:
        return generate_all_actions(state)

    def reset(self) -> List[Dict]:
        self.action_history = []
        self.action_option_history = []
        self.cur_step = 0
        self.cur_node = self.root
        self.history = [
            dict(
                state=self.initial_state,
                completed=self.cur_node.completed_subgoals,
                total=self.cur_node.total_subgoals,
            )
        ]
        return self.history

    def step(self, action: str) -> Tuple[List[Dict], bool]:
        self.action_history.append(action)
        self.action_option_history.append(self.cur_node.action_space)
        self.cur_step += 1
        self.cur_node = self.cur_node.find_child(action)
        assert self.cur_step == self.cur_node.depth
        self.history.append(
            dict(
                state=self.cur_node.self_state,
                action=action,
                completed=self.cur_node.completed_subgoals,
                total=self.cur_node.total_subgoals,
            )
        )
        done = (self.cur_node.completed_subgoals == self.cur_node.total_subgoals) or (self.cur_step >= self.max_steps)
        # if the game ends
        if done:
            # add task success/fail info
            if self.cur_node.completed_subgoals == self.cur_node.total_subgoals:
                self.history.append(
                    dict(status="success")
                )
            else:
                self.history.append(
                    dict(status="fail")
                )
        return self.history, done

    def update_prob(self, actions: List[str], new_probs: np.ndarray) -> None:
        return # DEBUG
        ind = len(new_probs)
        node = self.cur_node.father
        while ind >= 0:
            a_size = len(node.action_space)
            print(f'{Fore.GREEN}origin action{Style.RESET_ALL}', node.action_space)
            new_node_action_space: List[str] = actions[ind-a_size:]
            new_node_probs: np.ndarray = new_probs[ind-a_size:]
            print(f'{Fore.GREEN}new action space{Style.RESET_ALL}', new_node_action_space) # TODO:
            print(f'{Fore.GREEN}new reward{Style.RESET_ALL}', new_node_probs) # TODO:
            # compare action space
            assert node.action_space == new_node_action_space
            # normalize the new reward
            print(f'{Fore.GREEN}new probs{Style.RESET_ALL}', new_node_probs) # TODO:
            new_node_probs /= np.sum(new_node_probs)
            print(f'{Fore.GREEN}reward before{Style.RESET_ALL}', node.r) # TODO:
            print(f'{Fore.GREEN}new reward (normalized){Style.RESET_ALL}', new_node_probs) # TODO:
            # learn the new probs
            for i in range(a_size):
                node.r[node.action_space[i]] = node.r[node.action_space[i]] * (1-self.alpha_1) + \
                    new_node_probs[i] * self.alpha_1
            print(f'{Fore.GREEN}reward after{Style.RESET_ALL}', node.r) # TODO:
            ind -= a_size
            node = node.father

    def wrap_traj(self) -> str:
        node = self.cur_node
        # status judge
        if node.completed_subgoals == node.total_subgoals:
            trajectory = "[STATUS] Success."
        elif self.cur_step >= self.max_steps:
            trajectory = "[STATUS] Fail."
        else:
            trajectory = "[STATUS] Incomplete."
        trajectory = "[total subgoals] {}\n[completed subgoals] {}\n".format(node.total_subgoals, node.completed_subgoals) + trajectory
        trajectory = "[STATE {}] ".format(node.depth) + node.self_state + "\n" + trajectory
        while node.father is not None:
            trajectory = "[ACTION {}] ".format(node.depth) + node.father.find_action(node) + "\n" + trajectory
            node = node.father
            wrapped_r = ""
            for action in node.action_space:
                wrapped_r += "{\"action\": \"" + action + "\", \"probability\": " + "{:.2f}".format(node.r[action]) + "}\n"
            trajectory = "[PROBABILITY {}]\n".format(node.depth) + wrapped_r.strip("\n") + "\n" + trajectory
            trajectory = "[total subgoals] {}\n[completed subgoals] {}\n".format(node.total_subgoals, node.completed_subgoals) + trajectory
            trajectory = "[STATE {}] ".format(node.depth) + node.self_state + "\n" + trajectory
        trajectory = "[GOAL] " + self.goal_statement + "\n" + trajectory
        return trajectory

    def wrap_goal_traj(self) -> str:
        node = self.cur_node
        # status judge
        if node.completed_subgoals == node.total_subgoals:
            trajectory = "[STATUS] Success."
        elif self.cur_step >= self.max_steps:
            trajectory = "[STATUS] Fail."
        else:
            trajectory = "[STATUS] Incomplete."
        trajectory = "[completed subgoals] {}\n".format(node.est_goal) + trajectory
        trajectory = "[STATE {}] ".format(node.depth) + node.self_state + "\n" + trajectory
        while node.father is not None:
            trajectory = "[ACTION {}] ".format(node.depth) + node.father.find_action(node) + "\n" + trajectory
            node = node.father
            trajectory = "[completed subgoals] {}\n".format(node.est_goal) + trajectory
            trajectory = "[STATE {}] ".format(node.depth) + node.self_state + "\n" + trajectory
        trajectory = "[GOAL] " + self.goal_statement + "\n" + trajectory
        print(f'{Fore.GREEN}goal trajectory{Style.RESET_ALL}', trajectory)
        return trajectory

    def snapshot(self, log_folder_path: str, run_prefix: str):
        '''Take a snapshot of the current environment state and history'''
        # dump the searched space to json
        with open(
            os.path.join(log_folder_path, run_prefix + 'node_tree.json'), 'w') as f:
            json.dump(self.root.to_dict(), f, indent=4)
        # dump the history
        with open(
            os.path.join(log_folder_path, run_prefix + 'history.json'), 'w') as f:
            json.dump(self.history, f, indent=4)