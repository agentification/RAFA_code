import re
import random 

import logging

logger = logging.getLogger('llmmpc_tictactoe')

reg_state = r'''[1-9XO] \| [1-9XO] \| [1-9XO]
---------
[1-9XO] \| [1-9XO] \| [1-9XO]
---------
[1-9XO] \| [1-9XO] \| [1-9XO]'''

reg_oppo = r'''Tic-Tac-Toe Board:

[1-9XO] \| [1-9XO] \| [1-9XO]
---------
[1-9XO] \| [1-9XO] \| [1-9XO]
---------
[1-9XO] \| [1-9XO] \| [1-9XO]

Opponent's Move: "[XO]" in position [1-9]'''


def wrap_with_format(items, format):
    return ''.join(format.format(**x) for x in items)


def encode(state):
    return '\n---------\n'.join(
        f'{state[a] or a} | {state[b] or b} | {state[c] or c}' 
        for a, b, c in [('1', '2', '3'), ('4', '5', '6'), ('7', '8', '9')])


def decode(state):
    if state is None:
        return None
    state = {'1': state[0], '2': state[4], '3': state[8],
            '4': state[20], '5': state[24], '6': state[28],
            '7': state[40], '8': state[44], '9': state[48]}
    for key, value in state.items():
        if key == value:
            state[key] = None
    return state


def switch(role):
    return 'X' if role == 'O' else 'O'


def find_state(response):
    search = re.search(reg_state, response)
    assert search, response
    return search.group()


def find_action(response):
    # Usually action is the first token in response
    # However, sometimes the response of gpt has an extra ':' in the beginning
    search = re.search('[1-9]', response)
    if search:
        return search.group()
    else:
        ('WARNING: no actions found in response', response)
        return None


def find_actions(response):
    # Usually action is the first token in response
    # However, sometimes the response of gpt has an extra ':' in the beginning
    return re.findall('[1-9]', response)


def find_flag(response):
    if 'yes' in response.lower():
        return True
    elif 'no' in response.lower():
        return False
    else:
        raise ValueError(response)


class Buffer:
    def __init__(self, history=None, recent=1):
        if history:
            self._storage = history
        else:
            self._storage = []
        self.recent = recent
    
    def sample(self, k):
        if k == 0:
            return ''
        if len(self._storage) <= k - 1:
            samples = self._storage
        else:
            samples = random.sample(self._storage[:-self.recent], k=k-self.recent) + self._storage[-self.recent:]
        return ''.join(samples)
    
    def add(self, record):
        self._storage.append(record)
