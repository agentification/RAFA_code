from . import *
from functools import partial


def get_samples(env, history, x, y, n_generate_sample, prompt_sample, stop):
    if prompt_sample == 'standard':
        prompt = env.standard_prompt_wrap(x, y)
    elif prompt_sample == 'cot':
        prompt = env.cot_prompt_wrap(x, y)
    else:
        raise ValueError(f'prompt_sample {prompt_sample} not recognized')
    samples = gpt_with_history(prompt, history, n=n_generate_sample, stop=stop)
    return [y + _ for _ in samples]


class NaiveAgent(Agent):
    def __init__(self, backend, temperature, prompt_sample, method_generate, method_evaluate, method_select,
                 n_generate_sample,
                 n_evaluate_sample, n_select_sample):
        super().__init__()

        global gpt
        global gpt_with_history
        gpt = partial(gpt, model=backend)
        gpt_with_history = partial(gpt_with_history, model=backend)

        self.backend = backend
        self.prompt_sample = prompt_sample
        self.method_generate = method_generate
        self.method_evaluate = method_evaluate
        self.method_select = method_select
        self.n_generate_sample = n_generate_sample
        self.n_evaluate_sample = n_evaluate_sample
        self.n_select_sample = n_select_sample
        self.reflects = []
        self.value_reflects = []

    def plan(self, env, to_print=True):
        print(gpt)
        print(gpt_with_history)
        x = env.puzzle  # input
        prompt = "Now we would like to play a game of 24. That is, given 4 numbers, try to use them with arithmetic operations (+ - * /) to get 24. "
        obs = [prompt,
               {"feedback": "What you have learned about the game of 24 puzzle are summarized below.\n" + "\n".join(
                   self.reflects)}]

        # ys = get_samples(env, x, obs, '', self.n_generate_sample, self.prompt_sample, stop=None)
        ys = get_samples(env, obs, x, '', self.n_generate_sample, self.prompt_sample, stop=None)

        if to_print:
            print(ys)

        result = ys[0] if len(ys) else ys
        return result, {'proposals': ys}

    def reflect(self, env, obs):
        y = obs['answer']
        feedback = obs['feedback']
        reflect_prompt, value_reflect_prompt = env.reflect_prompt_wrap(env.puzzle, y, feedback)
        # reflects = gpt_with_history(reflect_prompt, obs, stop=None)
        # value_reflects = gpt_with_history(value_reflect_prompt, obs, stop=None)
        reflects = gpt(reflect_prompt, stop=None)
        value_reflects = gpt(value_reflect_prompt, stop=None)
        self.reflects.extend(reflects)
        self.value_reflects.extend(value_reflects)
        return

    def act(self, env, obs):
        if len(obs['feedback']) >= 1:
            self.reflect(env, obs)
        action, info = self.plan(env)
        return action, info

    def update(self, obs, reward, done, info):
        if done:
            self.reflects = []
            self.value_reflects = []
