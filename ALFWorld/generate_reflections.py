from utils import get_completion, get_completion_gpt3

from typing import List, Dict, Any

with open("./ours_new_feedback_examples.txt", 'r') as f:
    FEW_SHOT_EXAMPLES = f.read()

def _get_scenario(s: str) -> str:
    """Parses the relevant scenario from the experience log."""
    return s.split("Here is the task:")[-1].strip()

def _generate_reflection_query(log_str: str, memory: List[str]) -> str:
    """Allows the Agent to reflect upon a past experience."""
    scenario: str = _get_scenario(log_str)
    query: str = f"""You will be given the history of a past experience in which you were placed in an environment and given a task to complete. You were unsuccessful in completing the task. Do not summarize your environment, but rather think about what is wrong with the critic you generated. Devise a concise, new critic that accounts for your mistake with reference to specific critics that you should have generated. You will need this later when you are solving the same task. Give your plan after "Failure feedback:". Here are three example:

{FEW_SHOT_EXAMPLES}

{scenario}"""

    if len(memory) > 0:
        query += '\n\nPlans and critics from past attempts:\n'
        for i, m in enumerate(memory):
            query += f'Trial #{i}: {m}\n'

    query += '\n\nFailure feedback:'
    return query

def update_memory(trial_log_path: str, env_configs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Updates the given env_config with the appropriate reflections."""
    with open(trial_log_path, 'r') as f:
        full_log: str = f.read()
        
    env_logs: List[str] = full_log.split('#####\n\n#####')
    assert len(env_logs) == len(env_configs), print(f'bad: {len(env_logs)}, {len(env_configs)}')
    for i, env in enumerate(env_configs):
        # if unsolved, get reflection and update env config
        if not env['is_success'] and not env['skip']:
            if len(env['memory']) > 3:
                memory: List[str] = env['memory'][-3:]
            else:
                memory: List[str] = env['memory']
            reflection_query: str = _generate_reflection_query(env_logs[i], memory)
            reflection: str = get_completion(reflection_query) # type: ignore
            env_configs[i]['memory'] += [reflection]
                
    return env_configs


def update_memory_gpt3(trial_log_path: str, env_configs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Updates the given env_config with the appropriate reflections."""
    with open(trial_log_path, 'r') as f:
        full_log: str = f.read()

    env_logs: List[str] = full_log.split('#####\n\n#####')
    assert len(env_logs) == len(env_configs), print(f'bad: {len(env_logs)}, {len(env_configs)}')
    for i, env in enumerate(env_configs):
        # if unsolved, get reflection and update env config
        if not env['is_success'] and not env['skip']:
            if len(env['memory']) > 3:
                memory: List[str] = env['memory'][-3:]
            else:
                memory: List[str] = env['memory']
            reflection_query: str = _generate_reflection_query(env_logs[i], memory)
            reflection: str = get_completion_gpt3(reflection_query)  # type: ignore
            env_configs[i]['memory'] += [reflection]

    return env_configs