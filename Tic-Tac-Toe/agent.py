import os
import json
import random
from functools import partial

from api import API
from env import TicTacToe
from utils import *
from prompt import *


class BaseAgent:
    def __init__(self, role, api, backend='gpt-3.5-turbo', temperature=0.2, **kargs):
        self.role = role        # 'X' or 'O'
        self.backend = backend  # gpt-3.5-turbo or gpt-4
        self.temperature = temperature
        self.n = 1
        self.mpc = False
        self.api = api
        self.cur_game = ''
        self.saved_games = ''

    def save(self, *args, **kargs):
        pass

    def load(self, *args, **kargs):
        pass

    def update_oppo_model(self, *args, **kargs):
        pass

    def update_dynamics_model(self, *args, **kargs):
        pass

    def update_eval_model(self, *args, **kargs):
        pass

    def new_game(self):
        self.cur_game = initial_prompt

    def save_game(self):
        self.saved_games += self.cur_game

    def gpt(self, prompt, **kargs):
        logger.debug('-'*80)
        logger.debug(prompt)
        response = self.api.gpt(
            prompt, model=self.backend, temperature=self.temperature, **kargs)[0]
        logger.debug(response)
        logger.debug('-'*80)
        return response

    def step(self, state):
        # action_space = self.gpt(availablility_prompt.format(state=state))
        prompt = action_prompt.format(role=self.role, state=state)
        while True:
            response = self.gpt(prompt)
            action = find_action(response)
            if action in state:
                return action
            logger.error('Invalid action. Retry')
            prompt += action_fix_prompt.format(state=state, role=self.role, action=action)

    def add_self(self, action, next_state):
        self.cur_game += record_self_prompt.format(
            role=self.role, action=action, state=next_state)

    def add_oppo(self, action, next_state):
        self.cur_game += record_oppo_prompt.format(
            role=switch(self.role), action=action, state=next_state)

    def add_result(self, winner):
        if winner == self.role:
            self.cur_game += f'''Outcome: You win!'''
        elif winner == switch(self.role):
            self.cur_game += f'''Outcome: Opponent wins!'''
        else:
            self.cur_game += f'''Outcome: The game is a tie!'''

    def add_reflection(self):
        self.cur_game += improve_prompt
        self.cur_game += self.gpt(self.cur_game) + '\n\n'


class MPCAgent(BaseAgent):
    def __init__(self, *args, n=5, verbose=False, eval=False, **kargs):
        super(MPCAgent, self).__init__(*args, **kargs)
        self.n = n
        self.verbose = verbose
        self.mpc = True
        self.eval = eval

        self.find_oppo = partial(re.findall, reg_oppo)

        self.examples_dynamics = []
        self.examples_winner = []
        self.examples_complete = []
        self.examples_oppo = []
        self.memory = {}
        self.optimize()

    def load(self, path):
        if os.path.exists(path):
            with open(path) as f:
                saved = json.load(f)
            # self.improvement_plan = saved['improvement_plan']
            self.saved_games = saved['saved_games']
            self.examples_dynamics = saved['examples_dynamics']
            self.examples_winner = saved['examples_winner']
            self.examples_complete = saved['examples_complete']
            self.examples_oppo = saved['examples_oppo']
            self.memory = saved['memory']

    def save(self, path):
        record = {
            # 'improvement_plan': self.improvement_plan,
            'saved_games': self.saved_games,
            'examples_dynamics': self.examples_dynamics,
            'examples_winner': self.examples_winner,
            'examples_complete': self.examples_complete,
            'examples_oppo': self.examples_oppo,
            'memory': self.memory
        }
        with open(path, 'w') as f:
            json.dump(record, f)

    def optimize(self):
        self.improvement_plan = ''
        if self.saved_games:
            self.improvement_plan = self.gpt(
                optimize_prompt.format(saved_games=self.saved_games))
    
    def set_update_flag(self):
        for key in self.memory.keys():
            self.memory[key]['up_to_date'] = False

    def propose(self, state):
        # action_space = self.gpt(availablility_prompt.format(state=state))
        prompt = propose_prompt.format(
            improvement_plan=self.improvement_plan, 
            n=self.n, 
            role=self.role, 
            state=state, 
            # action_space=action_space
        )
        response = self.gpt(prompt)
        actions = find_actions(response.split('\n')[0])
        valid_actions = [action for action in actions if action in state]

        while not valid_actions:
            available_actions = ','.join(find_actions(state))
            actions = ','.join(actions)
            prompt += suggestion_fix_prompt.format(
                state=state, role=self.role, actions=actions, available_actions=available_actions)
            response = self.gpt(prompt)
            actions = find_actions(response.split('\n')[0])
            valid_actions = [action for action in actions if action in state]

        return valid_actions

    def oppo_model(self, state):
        examples = wrap_with_format(self.examples_oppo, example_oppo_prompt)
        # action_space = self.gpt(availablility_prompt.format(state=state))
        action = find_action(self.gpt(oppo_prompt.format(
            examples=examples, 
            role=switch(self.role), 
            state=state,
            # action_space=action_space
        )))
        return action

    def evaluate(self, state):
        flag_win_X, flag_win_O =self.winner_eval_model(state)
        if flag_win_X:
            return True, 1 if 'X' == self.role else -1
        elif flag_win_O:
            return True, 1 if 'O' == self.role else -1
        else:
            return (True, 0) if self.complete_eval_model(state) else (False, 0)
    
    def mcts(self, cur_prompt, cur_state):
        if cur_state in self.memory and self.memory[cur_state]['up_to_date']:
            return (self.memory[cur_state]['value'], 
                    self.memory[cur_state]['optimal_action'])
        search = []
        optimal = None
        actions = self.propose(cur_state)
        for action in actions:
            if not action in cur_state:
                logger.warning(
                    f'Invalid action {action} in state \n{cur_state}')
                continue
            prompt = cur_prompt
            state = self.dynamics_model(cur_state, self.role, action)
            record = record_self_prompt.format(
                role=self.role, action=action, state=state)
            prompt += record
            done, reward = self.evaluate(state)
            if done:
                search.append((reward, action))
            else:
                oppo_action = self.oppo_model(state)
                state = self.dynamics_model(
                    state, switch(self.role), oppo_action)
                record = record_oppo_prompt.format(
                    role=switch(self.role), action=oppo_action, state=state)
                prompt += record
                done, reward = self.evaluate(state)
                if done:
                    search.append((reward, action))
                else:
                    search.append((self.mcts(prompt, state)[0], action))
            if search[-1][0] == 1:  # win
                optimal = search[-1]
                break
        
        optimal = optimal or max(search)
        self.memory[cur_state] = {
            'optimal_action': optimal[1], 
            'value': optimal[0],
            'up_to_date': True
        }
        return optimal
    
    def dynamics_model(self, state, role, action):
        examples = wrap_with_format(self.examples_dynamics, example_dynamics_prompt)
        next_state = find_state(self.gpt(dynamics_prompt.format(
            examples=examples, state=state, role=role, action=action)))
        return next_state

    def complete_eval_model(self, state):
        # examples = wrap_with_format(self.examples_complete, example_complete_prompt)
        # response = self.gpt(complete_prompt.format(examples=examples, state=state))
        response = self.gpt(availablility_prompt.format(state=state))
        action_space = find_actions(response.split('\n')[0])
        return not action_space

    def winner_eval_model(self, state):
        examples = wrap_with_format(self.examples_winner, format=example_winner_prompt)
        cot_eval = self.gpt(evaluate_prompt.format(examples=examples, state=state))
        therefore = cot_eval.strip().split('\n')[-1]
        flag_win_X = 'X win' in therefore or '"X" win' in therefore or 'is "X"' in therefore
        flag_win_O = 'O win' in therefore or '"O" win' in therefore or 'is "O"' in therefore
        if flag_win_X and flag_win_O:
            logger.warning('Both player wins')
        if not flag_win_X and not flag_win_O:
            assert 'no winner' in therefore, therefore
        return flag_win_X, flag_win_O

    def update_dynamics_model(self, state, role, action, next_state):
        next_state_pred = self.dynamics_model(state, role, action)
        if next_state_pred != next_state:
            self.set_update_flag()
            update = {
                'state': state, 
                'role': role, 
                'action': action, 
                'next_state': next_state
            }
            logger.warning(
                f'{self.role} updates its dynamic model with the following example:\n'
                + example_dynamics_prompt.format(**update)
            )
            self.examples_dynamics.append(update)

    def update_oppo_model(self, state, action):
        if self.oppo_model(state) != action:
            self.set_update_flag()
            update = {
                'state': state,
                'role': switch(self.role),
                'action': action
            }
            logger.warning(
                f'{self.role} updates its opponent model with the following example:\n'
                + example_oppo_prompt.format(**update)
            )
            self.examples_oppo.append(update)

    def update_eval_model(self, state, done, winner):
        self.update_winner_eval_model(state, winner)
        # self.update_complete_eval_model(state, done and winner == 'no one')

    def update_winner_eval_model(self, state, winner):
        flag_win_X, flag_win_O = self.winner_eval_model(state)
        if (flag_win_X, flag_win_O) != (winner == 'X', winner == 'O'):
            self.set_update_flag()
            update = {
                'state': state, 
                'cot': TicTacToe(state).cot()
            }
            logger.warning(
                f'{self.role} updates its winner evaluation model with the following example:\n'
                + example_winner_prompt.format(**update)
            )
            self.examples_winner.append(update)

    # def update_complete_eval_model(self, state, flag):
    #     if self.eval:
    #         return
    #     if self.complete_eval_model(state) != flag:
    #         self.set_update_flag()
    #         self.examples_complete.append({
    #             'state': state, 
    #             'yes_or_no': 'Yes' if flag else 'No'
    #         })

    def step(self, state):
        value, action = self.mcts(self.cur_game, state)
        return action
