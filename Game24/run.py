import argparse
from agent.tot_agent import TreeOfThoughtAgent
from agent.naive_agent import NaiveAgent
from env.game24 import Game24
import os
from agent import gpt_usage
import json
import time


def run(args):
    agent_cls = {"tot": TreeOfThoughtAgent,
                 "naive": NaiveAgent,
                 "cot": NaiveAgent}.get(args.planning, NaiveAgent)
    agent = agent_cls(backend=args.backend, temperature=args.temperature, prompt_sample=args.prompt_sample,
                      method_generate=args.method_generate, method_evaluate=args.method_evaluate,
                      method_select=args.method_select, n_generate_sample=args.n_generate_sample,
                      n_evaluate_sample=args.n_evaluate_sample, n_select_sample=args.n_select_sample)
    env = Game24(args.task_file_path, args.feedback, args.max_step)
    cur_time = int(time.time())
    file = f'logs/lmmmpc/{args.task}/{args.backend}_{args.temperature}_{args.method_generate}{args.n_generate_sample}_{args.method_evaluate}{args.n_evaluate_sample}_{args.method_select}{args.n_select_sample}_start{args.task_start_index}_end{args.task_end_index}_{args.planning}_feedback_{args.feedback}time{cur_time}.json'
    
    os.makedirs(os.path.dirname(file), exist_ok=True)
    logs = []
    # for i in range(args.task_start_index, args.task_end_index):
    for i in range(args.task_end_index-1, args.task_start_index-1, -1):
        obs = env.reset(i)
        log = {'idx': i, 'agent_info': [], 'env_info': []}
        done = False
        while not done:
            action, agent_info = agent.act(env, obs)
            obs, reward, done, env_info = env.step(action)
            agent.update(obs, reward, done, env_info)
            log['agent_info'].append(agent_info)
            log['env_info'].append(env_info)
            print(obs)
            print(reward, done, env_info)
            log['usage_so_far'] = gpt_usage(args.backend)
            tmp_logs = logs + [log]
            with open(file, 'w') as f:
                json.dump(tmp_logs, f, indent=4)
        logs.append(log)
        with open(file, 'w') as f:
            json.dump(logs, f, indent=4)


def parse_args():
    args = argparse.ArgumentParser()
    args.add_argument('--backend', type=str,
                      choices=['gpt-4', 'gpt-3.5-turbo', 'gpt-3.5-turbo-16k', 'gpt-4-0613', 'text-davinci-003', 'text-davinci-002'],
                      default='gpt-3.5-turbo')
    args.add_argument('--temperature', type=float, default=0.7)

    args.add_argument('--task', type=str, required=True, choices=['game24', 'text', 'crosswords'])
    args.add_argument('--task_file_path', type=str, required=True)
    args.add_argument('--task_start_index', type=int, default=900)
    args.add_argument('--task_end_index', type=int, default=1000)

    args.add_argument('--naive_run', action='store_true')
    args.add_argument('--prompt_sample', type=str,
                      choices=['standard', 'cot'])  # only used when method_generate = sample, or naive_run

    args.add_argument('--method_generate', type=str, choices=['sample', 'propose'])
    args.add_argument('--method_evaluate', type=str, choices=['value', 'vote'])
    args.add_argument('--method_select', type=str, choices=['sample', 'greedy'])
    args.add_argument('--n_generate_sample', type=int, default=10)  # only thing needed if naive_run
    args.add_argument('--n_evaluate_sample', type=int, default=1)
    args.add_argument('--n_select_sample', type=int, default=1)
    args.add_argument('--feedback', action='store_true')
    args.add_argument('--planning', type=str, choices=['tot', 'cot', 'naive'], default='tot')
    args.add_argument('--max_step', type=int, default=20)

    args = args.parse_args()
    if args.planning == "naive":
        args.generate = "sample"
        args.prompt_sample = "standard"
    if args.planning == "cot":
        args.generate = "sample"
        args.prompt_sample = "cot"
    print("FeedBack is set to:", args.feedback)
    return args


if __name__ == '__main__':
    args = parse_args()
    print(args)
    run(args)
