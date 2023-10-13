"""Adapted from https://github.com/ysymyth/ReAct/blob/master/alfworld.ipynb"""

import os
import sys
import json
import yaml
import openai
import importlib
import alfworld
import alfworld.agents.environment
from env_history import EnvironmentHistory
from typing import List, Dict, Any, Tuple
from statistics import mean
import math
import copy
from tenacity import retry, stop_after_attempt, retry_if_exception_type, retry_if_not_exception_type
import time, random, re

FOLDER = './prompts'
PROMPT_FILE = 'alfworld_newprompts.json' #'alfworld_3prompts.json'
VALUE_PROMPT_FILE = 'alfworld_value.json'
openai.api_key = os.getenv("OPENAI_API_KEY", "")

with open(os.path.join(FOLDER, PROMPT_FILE), 'r') as f:
    d = json.load(f)

with open(os.path.join(FOLDER, VALUE_PROMPT_FILE), 'r') as f:
    value_d = json.load(f)

@retry(
    stop=stop_after_attempt(4),
    retry=retry_if_not_exception_type((ValueError, OSError))
)
def call_openai_api(prompt, stop, n, temperature=0.0, chatcompletion=False):
    if chatcompletion:
        response = openai.ChatCompletion.create(
            engine='gpt-35-turbo',
            messages=[
                {"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=100,
            top_p=0.8,
            stop=stop,
        )
    else:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            logprobs=0,
            temperature=temperature,
            max_tokens=100,
            top_p=0.8,
            n=n,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=stop,
        )
    time.sleep(0.2)
    return response

def llm(prompt, stop=["\n"], n=1, temperature=0.0, chatcompletion=False):
    try:
        response = call_openai_api(prompt, stop, n=n, temperature=temperature, chatcompletion=chatcompletion)
    except Exception as e:
        response = {}
    if chatcompletion:
        for tries in range(1, 8):
            if response == {}:
                response = call_openai_api(prompt, stop, n=n, temperature=temperature, chatcompletion=chatcompletion)
            elif all(item["message"]['content'].strip() == '' for item in response["choices"]):
                    response = call_openai_api(prompt, stop, n=n, temperature=temperature, chatcompletion=chatcompletion)
            else:
                break
        return response["choices"][0]["message"]["content"].strip()
    else:
        for tries in range(1, 8):
            if response == {}:
                response = call_openai_api(prompt, stop, n=n, temperature=temperature, chatcompletion=chatcompletion)
            elif all(item["text"].strip() == '' for item in response["choices"]):
                    response = call_openai_api(prompt, stop, n=n, temperature=temperature, chatcompletion=chatcompletion)
            else:
                break
        return response["choices"][0]["text"].strip()


def llm_n(prompt, stop=["\n"], n=6, temperature=1.0):
    try:
        response = call_openai_api(prompt, stop, n=n, temperature=temperature)
    except Exception as e:
        response = {}
    for tries in range(1, 8):
        if response == {}:
            response = call_openai_api(prompt, stop, n=n, temperature=temperature)
        elif all(item["text"].strip() == '' for item in response["choices"]):
                response = call_openai_api(prompt, stop, n=n, temperature=temperature)
        else:
            break
    response_list = []
    for choice in response["choices"]:
        try:
            response_text = choice["text"].strip()
            response_prob = math.exp(mean(choice["logprobs"]["token_logprobs"]))
            response_list.append((response_text, response_prob))
        except Exception as e:
            pass
    if n > 1:
        response_list = sorted(response_list, key=lambda x: x[1], reverse=True)
    return response_list

def process_ob(ob):
    if ob.startswith('You arrive at loc '):
        ob = ob[ob.find('. ')+2:]
    return ob

sample_per_node = 2
depth = 2  # depth - 1, as the first layer is not counted
replan = True
def alfworld_run(env, base_prompt, value_prompt, memory: List[str], to_print=True, ob='', init_admaction=None, task=None, z=0) -> Tuple[EnvironmentHistory, bool]:
    if len(memory) > 3:
        env_history = EnvironmentHistory(base_prompt, ob, memory[-3:], [])
        env_value_history = EnvironmentHistory(value_prompt, ob, memory[-3:], [])
    else:
        env_history = EnvironmentHistory(base_prompt, ob, memory, [])
        env_value_history = EnvironmentHistory(value_prompt, ob, memory, [])
    receptacle_list = [init_a.replace('go to ', '') for init_a in init_admaction]
    env_history.reset()
    env_value_history.reset()
    if to_print:
        print(ob)
        sys.stdout.flush()
    cur_step = 0
    env_value_estimate = 0.0
    gamma = 0.9
    task_class, task_name = task
    while cur_step < 20:
        temp_history = [copy.deepcopy(env_history) for _ in range(sample_per_node ** depth)]
        temp_value_history = [copy.deepcopy(env_value_history) for _ in range(sample_per_node ** depth)]
        value_estimate = [env_value_estimate for _ in range(sample_per_node ** depth)]
        temp_admaction = [copy.deepcopy(init_admaction) for _ in range(sample_per_node ** depth)]
        for dep in range(depth):
            layer_samples = sample_per_node ** dep
            for parent_idx in range(layer_samples):
                parent_effective_start_idx = sample_per_node ** (depth - dep) * parent_idx
                value_response = llm(str(temp_value_history[parent_effective_start_idx]) + "\n>", stop=['\n'], chatcompletion=False)
                if cur_step != 0 or dep != 0:
                    no_receptacle = True
                    step_idx = 1
                    while no_receptacle:
                        receptacle = [loc for loc in receptacle_list if
                                      (loc in temp_history[parent_effective_start_idx]._history[-step_idx]['value'])]
                        step_idx += 1
                        no_receptacle = not receptacle
                    receptacle = receptacle[-1]
                    objects = re.findall(r'(\b\w+\b)\s+(\d+)',
                                         temp_history[parent_effective_start_idx]._history[-1]['value'].replace(receptacle, ''))
                    object_list = [' '.join(object) for object in objects]
                    temp_admaction[parent_effective_start_idx].append(f'open {receptacle}')

                    hold_object = [obj['value'] for obj in temp_history[parent_effective_start_idx]._history if obj['value'].startswith('You pick up the')]
                    put_object = [obj['value'] for obj in temp_history[parent_effective_start_idx]._history if obj['value'].startswith('You put the')]
                    for obj in object_list:
                        if obj.startswith('desklamp'):
                            temp_admaction[parent_effective_start_idx].append(f'use {obj}')
                        elif len(hold_object) == len(put_object):
                            temp_admaction[parent_effective_start_idx].append(f'take {obj} from {receptacle}')
                    if len(hold_object) > len(put_object):
                        hold_object = hold_object[-1].replace('You pick up the', '').split('from')[0].strip()
                        temp_admaction[parent_effective_start_idx].append(f'put {hold_object} in/on {receptacle}')
                        if receptacle.startswith('fridge'):
                            temp_admaction[parent_effective_start_idx].append(f'cool {hold_object} with {receptacle}')
                        if receptacle.startswith('microwave'):
                            temp_admaction[parent_effective_start_idx].append(f'heat {hold_object} with {receptacle}')
                        if receptacle.startswith('sinkbasin'):
                            temp_admaction[parent_effective_start_idx].append(f'clean {hold_object} with {receptacle}')
                random.shuffle(temp_admaction[parent_effective_start_idx])

                response_list = llm_n(str(temp_history[parent_effective_start_idx]) + "\n>", stop=['\n'])
                response_list = list(dict(response_list).items())
                response_list = [key for key, res in response_list if key in temp_admaction[parent_effective_start_idx]]
                response_list = response_list + temp_admaction[parent_effective_start_idx][:sample_per_node - len(response_list)]
                for i, admissable_action in enumerate(response_list[:sample_per_node]):
                    effect_start_idx = parent_effective_start_idx + sample_per_node ** (depth - dep - 1) * i
                    effect_end_idx = parent_effective_start_idx + sample_per_node ** (depth - dep - 1) * (i + 1)
                    temp_history[effect_start_idx].add("action", admissable_action)
                    observation = llm(str(temp_history[effect_start_idx]) + "\n", stop=['\n'], chatcompletion=False)  # predictive model
                    if observation == '':
                        observation = 'Nothing happens.'
                    for env_id in range(effect_start_idx, effect_end_idx):
                        if env_id != effect_start_idx:
                            temp_history[env_id].add("action", admissable_action)
                        temp_history[env_id].add("observation", observation)

                        if value_response.startswith('critic:'):
                            temp_value_history[env_id].add("critic", value_response)
                            str_value = value_response.partition('=')[-1]
                            try:
                                value_estimate[env_id] = float(str_value[:-1]) * gamma ** dep
                            except Exception as e:
                                pass
                        temp_value_history[env_id].add("action", "OK.")
                        temp_value_history[env_id].add("observation", observation)
                        if dep == depth - 1:  # terminal value
                            value_response = llm(str(temp_value_history[env_id]) + "\n>", stop=['\n'], chatcompletion=False)
                            if value_response.startswith('critic:'):
                                temp_value_history[env_id].add("critic", value_response)
                                str_value = value_response.partition('=')[-1]
                                try:
                                    value_estimate[env_id] = float(str_value[:-1]) * gamma ** dep
                                except Exception as e:
                                    pass
        argmax = value_estimate.index(max(value_estimate))
        print(value_estimate)
        rollout = 1 if replan else (len(temp_history[argmax]._history)-len(env_history._history)) // 2
        for _ in range(rollout):
            action = temp_history[argmax]._history[len(env_history._history)]['value']
            if len(temp_value_history[argmax]._history) > len(env_value_history._history):
                value_response = llm(str(env_value_history) + "\n>", stop=['\n'], chatcompletion=False)
                if value_response.startswith('critic'):
                    env_value_history.add("critic", value_response)
                    str_value = value_response.partition('=')[-1]
                    try:
                        env_value_estimate = float(str_value[:-1])
                    except Exception as e:
                        pass
                    print(value_response)
            observation, reward, done, info = env.step([action])
            observation, reward, done = process_ob(observation[0]), info['won'][0], done[0]
            env_value_history.add("action", 'OK.')
            env_value_history.add("observation", observation)

            env_history.add("action", action)
            env_history.add("observation", observation)
            if to_print:
                print(f'{cur_step}> {action}\n{observation}')
                sys.stdout.flush()
            if reward:
                return env_value_history, True
            cur_step += 1
    return env_value_history, False

PREFIXES = {
    'pick_and_place': 'put',
    'pick_clean_then_place': 'clean',
    'pick_heat_then_place': 'heat',
    'pick_cool_then_place': 'cool',
    'look_at_obj': 'examine',
    'pick_two_obj': 'puttwo'
}

def run_trial(
        trial_log_path: str,
        world_log_path: str,
        trial_idx: int,
        env_configs: List[Dict[str, Any]],
        use_memory: bool
    ) -> List[Dict[str, Any]]:
    importlib.reload(alfworld)
    importlib.reload(alfworld.agents.environment)

    with open('base_config.yaml') as reader:
        config = yaml.safe_load(reader)
    split = "eval_out_of_distribution"

    env = getattr(alfworld.agents.environment, config["env"]["type"])(config, train_eval=split)
    temp_envs_before_init = [copy.deepcopy(env) for _ in range(sample_per_node ** depth)]
    env = env.init_env(batch_size=1)

    num_successes: int = 0
    num_additional_successes: int = 0
    num_envs: int = len(env_configs)

    for z, env_config in enumerate(env_configs):
        print(f'{z} / {len(env_configs)}')
        ob, info = env.reset()
        init_admaction = info['admissible_commands'][0][:-2]

        ob = '\n'.join(ob[0].split('\n\n')[1:])
        name = '/'.join(info['extra.gamefile'][0].split('/')[-3:-1])

        print(f"using {name}")

        if env_config["is_success"]:
            num_successes += 1

            # log to world log
            with open(world_log_path, 'a') as wf:
                wf.write(f'Environment #{z} Trial #{trial_idx}: SUCCESS\n')
            with open(trial_log_path, 'a') as wf:
                wf.write(f'\n#####\n\nEnvironment #{z}: Success\n\n#####\n')
            continue

        for i, (k, v) in enumerate(PREFIXES.items()):
            if name.startswith(k):
                if trial_idx == 0:
                    base_prompt = 'Interact with a household to solve a task. Here are two examples.\n' + d[f'act_{v}_1'] + d[f'act_{v}_0']
                else:
                    base_prompt = 'Interact with a household to solve a task. Here are two examples.\n' + d[f'act_{v}_2'] + d[f'act_{v}_0']
                value_prompt = 'You are a value critic of states in a household task. Here are two examples.\n' + value_d[f'value_{v}_1'] + value_d[f'value_{v}_0']
                final_env_history, is_success = alfworld_run(env, base_prompt, value_prompt, env_config["memory"] if use_memory else [],
                                                             to_print=True, ob=ob, init_admaction=init_admaction, task=(name, v), z=z)

                # update env config
                if is_success:
                    status_str: str = f'Environment #{z} Trial #{trial_idx}: SUCCESS'
                    env_configs[z]['is_success'] = True
                    num_successes += 1
                    num_additional_successes += 1
                else:
                    status_str: str = f'Environment #{z} Trial #{trial_idx}: FAIL'

                # log to world log
                with open(world_log_path, 'a') as f:
                    f.write(status_str + '\n')

                # log env results to trial log
                with open(trial_log_path, 'a') as wf:
                    final_env_history = str(final_env_history).replace(value_prompt, '')
                    wf.write(f'\n#####\n\nEnvironment #{z}:\n{final_env_history}\n\nSTATUS: {"OK" if is_success else "FAIL"}\n\n#####\n')

    # close environment object
    env.close()

    # log trial results to trial and world logs
    log_str: str = f"""
-----
SUCCESS: {num_successes}
ADDITIONAL SUCCESS: {num_additional_successes}
FAIL: {num_envs - num_successes}
TOTAL: {num_envs}
ACCURACY: {round(num_successes / num_envs, 2)}
-----"""
    with open(trial_log_path, 'a') as wf:
        wf.write(log_str)
    with open(world_log_path, 'a') as wf:
        wf.write(log_str + '\n')

    return env_configs
