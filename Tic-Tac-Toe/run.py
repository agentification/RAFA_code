from api import API
from utils import *
from env import TicTacToe
from agent import BaseAgent, MPCAgent

import os
import json
import logging
import argparse
from tqdm import trange
from functools import partial

OUTPUT = 'output'


def parse_args():
    parser = argparse.ArgumentParser(description='Run experiments')
    parser.add_argument(
        '--X',
        type=str,
        default='gpt-3.5-turbo-16k',
        choices=['gpt-3.5-turbo', 'gpt-3.5-turbo-16k', 'gpt-3.5-turbo-instruct', 'gpt-35-turbo', 'gpt-4'],
        help='Backend GPT model for X player',
    )
    parser.add_argument(
        '--O',
        type=str,
        default='gpt-3.5-turbo-16k',
        choices=['gpt-3.5-turbo', 'gpt-3.5-turbo-16k', 'gpt-3.5-turbo-instruct', 'gpt-35-turbo', 'gpt-4'],
        help='Backend GPT model for O player',
    )
    parser.add_argument(
        '--X_MPC',
        type=int,
        default=1,
        help='Number of proposed actions each step for MPC. Default: No MPC'
    )
    parser.add_argument(
        '--O_MPC',
        type=int,
        default=1,
        help='Number of proposed actions each step for MPC. Default: 1 (No MPC)'
    )
    parser.add_argument(
        '--temperature',
        type=float,
        default=0.2,
        help='GPT temperature for action proposing'
    )
    parser.add_argument(
        '--eval_freq',
        type=int,
        default=1,
        help='Evaluation frequency. Default: 1 (evaluate after every training epoch)'
    )
    parser.add_argument(
        '--num_train_epochs',
        type=int,
        default=1,
        help='Number of rounds to battle. Default: 1 ()'
    )
    parser.add_argument(
        '--num_eval_epochs',
        type=int,
        default=1,
        help='Number of rounds to battle'
    )
    parser.add_argument(
        '--verbose',
        type=int,
        default=1,
        help='Auxiliary output level'
    )
    parser.add_argument(
        '--bd_api',
        action='store_true'
    )
    args = parser.parse_args()
    return args


def battle(X, O, eval=False, verbose=False):
    env = TicTacToe()
    state = encode(env.reset())
    X.new_game()
    O.new_game()
    done = False
    player = {'X': X, 'O': O}
    role = 'O'
    if verbose:
        logger.info('Initial board:')
        logger.info(state)
    while not done:
        role = switch(role)
        action = player[role].step(state)
        next_state, win, done, _ = env.step(action, role)
        next_state = encode(next_state)
        player[role].add_self(action, next_state)
        player[switch(role)].add_oppo(action, next_state)
        winner = role if win else 'no one'
        if not eval:
            player[switch(role)].update_oppo_model(state, action)
            for r in ['X', 'O']:
                player[r].update_dynamics_model(state, role, action, next_state)
                player[r].update_eval_model(state, done, winner)
        state = next_state
        if verbose:
            logger.info(f"{role} takes action {action}")
            logger.info("Updated board:")
            logger.info(next_state)
    winner = role if win else 'Tie'
    for r in ['X', 'O']:
        player[r].add_result(winner)
        if player[r].mpc:
            player[r].add_reflection()
    X_record, O_record = X.cur_game, O.cur_game
    if not eval:
        X.save_game()
        O.save_game()
    if verbose:
        if winner != 'Tie':
            logger.info(f'{role} wins!')
        else:
            logger.info('Tie!')
    return winner, X_record, O_record


def get_logger(output_name):
    logger = logging.getLogger('llmmpc_tictactoe')
    logger.setLevel(logging.DEBUG)
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = logging.FileHandler(filename=f'{output_name}.log', mode='w')
    file_handler.setLevel(logging.DEBUG)
    # file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stdout_handler = logging.StreamHandler()
    stdout_handler.setLevel(logging.INFO)
    # stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)

    return logger


def evaluate(X, O, eval_path, num_eval_epochs, verbose=False):
    eval_winners = []
    eval_X_buffer = []
    eval_O_buffer = []
    if os.path.exists(eval_path):
        with open(eval_path) as f:
            eval_info = json.load(f)
            eval_winners = eval_info['winner']
            eval_X_buffer = eval_info['X']
            eval_O_buffer = eval_info['O']

    for epoch in range(len(eval_winners), num_eval_epochs):
        logger.info(f'====================== Start of Evaluation Epoch {epoch} ======================')
        winner, X_record, O_record = battle(X, O, eval=True, verbose=verbose)
        logger.info(f'[GPT usage] {api.gpt_usage()}')
        logger.info(f'====================== Evaluation Epoch {epoch} winner: {winner} ======================')

        eval_winners.append(winner)
        eval_X_buffer.append(X_record)
        eval_O_buffer.append(O_record)

        with open(eval_path, 'w') as f:
            json.dump({
                'winner': eval_winners, 
                'X': eval_X_buffer, 
                'O': eval_O_buffer
            }, f, indent=4)


if __name__ == '__main__':
    args = parse_args()
    note = ''
    note += f'MPC{args.X_MPC}_' if args.X_MPC > 1 else 'Base_'
    note += args.X
    note += '_vs_'
    note += f'MPC{args.O_MPC}_' if args.O_MPC > 1 else 'Base_'
    note += args.O
    note += f'_temp{args.temperature}'
    output = os.path.join(OUTPUT, note)
    os.makedirs(output, exist_ok=True)
    logger = get_logger(os.path.join(output, 'output'))
    logger.info(f"Simulate {args.X} vs {args.O} for {args.num_train_epochs} rounds.")

    winners, X_buffer, O_buffer = [], [], []
    
    with open('../../KEYLIST.json') as f:
        api = API(*json.load(f))
        
    if args.X_MPC > 1:
        X = MPCAgent('X', api, args.X, args.temperature, n=args.X_MPC)
    else:
        X = BaseAgent('X', api, args.X, args.temperature)
    if args.O_MPC > 1:
        O = MPCAgent('O', api, args.O, args.temperature, n=args.O_MPC)
    else:
        O = BaseAgent('O', api, args.O, args.temperature)

    evaluate(X, O, os.path.join(output, 'eval.json'), 
             args.num_eval_epochs, args.verbose)

    for epoch in range(args.num_train_epochs):
        subdir = os.path.join(output, str(epoch))
        os.makedirs(subdir, exist_ok=True)
        train_path = os.path.join(subdir, 'train.json')
        if os.path.exists(train_path):
            with open(train_path) as f:
                train_info = json.load(f)
                winners = train_info['winner']
                X_buffer = train_info['X']
                O_buffer = train_info['O']
            X.load(os.path.join(subdir, 'X.json'))
            O.load(os.path.join(subdir, 'O.json'))
        else:
            logger.info(f'====================== Start of Training Epoch {epoch} ======================')
            winner, X_record, O_record = battle(X, O, eval=False, verbose=args.verbose)
            X.save(os.path.join(subdir, 'X.json'))
            O.save(os.path.join(subdir, 'O.json'))
            logger.info(f'[GPT usage] {api.gpt_usage()}')
            logger.info(f'====================== Training Epoch {epoch} winner: {winner} ======================')

            winners.append(winner)
            X_buffer.append(X_record)
            O_buffer.append(O_record)

        with open(train_path, 'w') as f:
            json.dump({
                'winner': winners, 
                'X': X_buffer, 
                'O': O_buffer
            }, f, indent=4)

        if (epoch + 1) % args.eval_freq == 0:
            eval_path = os.path.join(subdir, 'eval.json')
            evaluate(X, O, eval_path, args.num_eval_epochs, args.verbose)
