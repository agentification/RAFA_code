import re
import torch
from typing import Union, List


def extract_color(s: str) -> Union[str, None]:
    match = re.search(r'the (\w+) block', s)
    if match:
        return match.group(1)
    return None


def extract_block(s: str) -> str:
    return "the {} block".format(
        extract_color(s)
    )


def extract_topper(target: str, state: str) -> str:
    match = re.search(r'the (\w+) block is on top of ' + target, state)
    return "the {} block".format(
        match.group(1)
    )


def count_obstacles(target: str, state: str) -> int:
    if "is holding " + target in state or target + " is in the hand" in state:
        return 0
    cnt = 0
    while True:
        if target + " is clear" in state:
            return cnt
        cnt += 1
        target = extract_topper(target, state)


def extract_integers_from_string(s) -> List[int]:
    # Use regex to find all integers in the string
    integers = re.findall(r'\d+', s)
    
    # Convert the extracted strings to integers
    return [int(i) for i in integers]


def llm_count_obstacles(target: str, state: str, world_model) -> int:
    prompt="I am playing with a set of blocks where I need to arrange the blocks into stacks. Here are the actions I can do \n\nPick up a block \nUnstack a block from on top of another block \nPut down a block \nStack a block on top of another block \n\nI have the following restrictions on my actions:\nI can only pick up or unstack one block at a time. \nI can only pick up or unstack a block if my hand is empty. \nI can only pick up a block if the block is on the table and the block is clear. A block is clear if the block has no other blocks on top of it and if the block is not picked up. \nI can only unstack a block from on top of another block if the block I am unstacking was really on top of the other block. \nI can only unstack a block from on top of another block if the block I am unstacking is clear. Once I pick up or unstack a block, I am holding the block. \nI can only put down a block that I am holding. \nI can only stack a block on top of another block if I am holding the block being stacked. \nI can only stack a block on top of another block if the block onto which I am stacking the block is clear. Once I put down or stack a block, my hand becomes empty.\n\nAfter being given a state and a target block in question, check if how many blocks are piled on the target block in the state.\n[STATE]I have that, the blue block is in the hand, the orange block is clear, the hand is holding the blue block, the orange block is on top of the red block, the red block is on top of the yellow block, and the yellow block is on the table.\nQuestion:how many blocks are piled on the blue block?\n[STATE STATUS]The key information in the state includes: \"the blue block is in the hand\". There are 0 block piled on the blue block.\n[STATE]I have that, the blue block is clear, the red block is clear, the white block is clear, the hand is empty, the red block is on top of the yellow block, the yellow block is on top of the orange block, the blue block is on the table, the orange block is on the table, and the white block is on the table.\nQuestion:how many blocks are piled on the orange block?\n[STATE STATUS]The key information in the state includes: \"the yellow block is on top of the orange block\", \"the red block is on top of the yellow block\". There are 2 block piled on the orange block.\n[STATE]I have that, the red block is clear, the yellow block is clear, the hand is empty, the blue block is on top of the white block, the red block is on top of the orange block, the yellow block is on top of the blue block, the orange block is on the table, and the white block is on the table.\nQuestion:how many blocks are piled on the blue block?\n[STATE STATUS]The key information in the state includes: \"the yellow block is on top of the blue block\". There is 1 block piled on the blue block.\n[STATE]{}\nQuestion:how many blocks are piled on {}?\n[STATE STATUS]".format(state, target)
    state_status = world_model.query_LM(prompt)
    ans = extract_integers_from_string(state_status)
    if len(ans) > 0:
        return ans[-1]
    return 0


def generate_all_actions(state):
    return_list = []
    if "hand is empty" in state:
        block = re.findall("the [a-z]{0,10} block is clear", state)
        block_color = [re.search("the ([a-z]{0,10}) block is clear", b).group(1) for b in block]
        # print(block_color)
        for c in block_color:
            # print("looking for", c)
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
    # print("input state:", state)
    if "and the " in state and ", and the" not in state:
        state = state.replace("and the ", ", and the ")
    states = state.split(", ")
    states = [s.strip()[4:].strip(".") if s.strip().startswith("and ") else s.strip().strip(".") for s in states]
    # print("state", states)

    changes = change.lower().strip().strip(".").split(", ")
    # print("initial states:", states)
    for c in changes:
        if c.startswith("and "):
            c = c[4:]
        success = 0
        # print("current change", c)
        if c.startswith("the hand"):
            # 防止llm重复说话
            if "and" not in c or "was" not in c or "now" not in c:
                continue
            # print(c)
            old = c.split("was")[1].split("and")[0].strip()
            # print(old)
            new = c.split("now")[1].strip()
            # print(new)
            for idx in range(len(states)):
                # print("=", s)
                if ("hand is " + old) in states[idx]:
                    # print(":", s)
                    states[idx] = states[idx].replace(old, new)
                    success += 1
                    # print(s)
        else:
            
            colors = re.findall(r"the (\w+) block", c)
            if len(colors) == 0:
                print("Error: zero-colors")
                print(c)
                torch.distributed.barrier()
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
                torch.distributed.barrier()
                raise Exception("ERROR")
        if success == 0:
            # print("ERROR")
            print("Error: no successful change")
            print(c)
            print(states)
            torch.distributed.barrier()
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
            torch.distributed.barrier()
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
