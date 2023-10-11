from copy import deepcopy
from utils import decode


class TicTacToe:
    initial_state = {str(i + 1): None for i in range(9)}
    lines = [
            ('1', '2', '3'), ('4', '5', '6'), ('7', '8', '9'),  # horizontal
            ('1', '4', '7'), ('2', '5', '8'), ('3', '6', '9'),  # vertical
            ('1', '5', '9'), ('3', '5', '7'),                   # horizontal
    ]
    names = [
        'First row', 'Second row', 'Third row',
        'First column', 'Second column', 'Third column',
        'Main diagonal', 'Anti-diagonal'
    ]
    
    def __init__(self, state=None):
        self.state = decode(state) or deepcopy(self.initial_state)
    
    def cot(self):
        cot = ''
        for (i, j, k), name in zip(self.lines, self.names):
            x, y, z = self.state[i] or i, self.state[j] or j, self.state[k] or k
            cot += f'{name}: {x} {y} {z}, '
            if x == y and x == z:
                return cot + f'{x} wins\n\nTherefore, {x} wins.'
            else:
                cot += f'no winner\n'
        return cot + '\n\nTherefore, there is no winner.'
    
    def reset(self):
        self.state = deepcopy(self.initial_state)
        return self.state
    
    def _win(self, role):
        for i, (p1, p2, p3) in enumerate(self.lines):
            if self.state[p1] == role and self.state[p2] == role and self.state[p3] == role:
                return True, self.names[i]
        return False, None

    def win(self, role):
        return self._win(role)[0]
    
    def done(self):
        for pos, val in self.state.items():
            if not val:
                return False
        return True
    
    def step(self, action, role):
        assert role in ['X', 'O'], role
        assert not self.state[action], (action, self.state)
        self.state[action] = role
        win = self.win(role)
        return self.state, win, win or self.done(), None  # state, reward, done, info
