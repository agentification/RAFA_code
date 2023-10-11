from env import Environment, DATA_PATH
import os
import pandas as pd
from env.util import *
from prompts.game24 import *


def get_current_numbers(y: str) -> str:
    last_line = y.strip().split('\n')[-1]
    return last_line.split('left: ')[-1].split(')')[0]


class Game24(Environment):
    def __init__(self, datadir, feedback=True, max_steps=20):
        """
                file: a csv file (fixed)
        """
        super().__init__()
        self.value_cache = {}
        path = os.path.join(DATA_PATH, '24', datadir)
        self.data = list(pd.read_csv(path)['Puzzles'])
        self.max_steps = max_steps
        self.index = 0
        self.puzzle = self.data[self.index]
        self.history = []
        self.feedbacks = []
        self.cur_step = 0
        self.feedback = feedback

    def reset(self, idx: int):
        self.index = idx
        self.puzzle = self.data[idx]
        self.history = []
        self.feedbacks = []
        self.cur_step = 0
        return {"action": "", "feedback": []}

    def check_step(self, idx, last_step, cur_step):
        try:
            if "answer" in cur_step.lower():
                correct, feedback = check_answer(self.puzzle, cur_step)
                if not correct:
                    return f"Step {idx} tries to give an answer but it is incorrect. {feedback}", 0
                return f"Step {idx} is correct. {feedback}", 10
            else:
                # Check if the step is valid
                correct, feedback = check_valid_move(idx, last_step, cur_step)
                if not correct:
                    return f"Step {idx} is illegal. {feedback}", 0

                formula = cur_step.split('left:')[0].strip("()")
                correct, feedback = check_equation(formula)
                if not correct:
                    return f"Step {idx} is not correctly calculated. {feedback}", 0

                correct, feedback = check_twentyfour(cur_step)
                if not correct:
                    return f"Step {idx} is impossible to lead to 24. {feedback}", 0

                return f"Step {idx} is correct and can lead to 24.", 1

        except Exception as e:
            print(e)
            return f"Step {idx} is invalid.", 0

    def generate_feedback(self, action):
        feedbacks = ["Evaluation:"]   # feedbacks for each step
        rewards = 0
        if isinstance(action, list):
            action = action[0]
        actions = action.strip(" \n").split('\n')
        idx = len(self.history)

        for action in actions:
            if idx == 0:
                last_step = self.puzzle
            else:
                last_step = self.history[-1]
            print(last_step)
            # print(action)
            if self.feedback:
                idx += 1
            feedback, reward = self.check_step(idx, last_step, action)
            if self.feedback:
                self.feedbacks.append(feedback)
                feedbacks.append(feedback)
            if reward > 0:
                if self.feedback:
                    self.history.append(action)
                rewards += reward
            else:
                break
        # if 'answer' not in steps[-1].lower():
        #     feedbacks.append("The answer is not complete.")
        total_feedback = " ".join(feedbacks) if self.feedback else None
        return total_feedback, rewards

    def step(self, action):
        self.cur_step += 1
        prev_len = len(self.history)
        feedback, reward = self.generate_feedback(action)
        new_len = len(self.history)
        delta = new_len - prev_len + 1 if new_len < 4 else new_len - prev_len
        assert delta > 0
        done = (reward >= 10) or (self.cur_step > self.max_steps)
        answer = [f"Step {i + 1}: {x}" for i, x in enumerate(action.split('\n')[:delta]) if x != ""]
        answer = "Attempt answer: " + "\n".join(answer)
        if self.feedback:
            info = {'action': action, 'history': self.history}
            obs = {'answer': answer, 'feedback': feedback}
        else:
            info = {'action': action, 'history': []}
            obs = {'answer': answer, 'feedback': []}
        return obs, reward, done, info

    @staticmethod
    def standard_prompt_wrap(x: str, y: str = '') -> str:
        return standard_prompt.format(input=x) + y

    @staticmethod
    def cot_prompt_wrap(x: str, y: str = '') -> str:
        return cot_prompt.format(input=x) + y

    @staticmethod
    def propose_prompt_wrap(x: str, y: str = '') -> str:
        current_numbers = get_current_numbers(y if y else x)
        if current_numbers == '24':
            prompt = cot_prompt.format(input=x) + 'Steps:\n' + y
            # print([prompt])
        else:
            prompt = propose_prompt.format(input=current_numbers)
        return prompt

    @staticmethod
    def validation_prompt_wrap(x: str, y: str) -> str or None:
        last_line = y.strip().split('\n')[-1]
        if 'left: ' not in last_line:  # last step
            return
        if len(y.strip().split('\n')) > 1:
            prev_line = get_current_numbers(y.strip().split('\n')[-2])
        else:
            prev_line = x
        return validation_prompt.format(input=prev_line, formula=last_line)

    @staticmethod
    def value_prompt_wrap(x: str, y: str) -> str:
        last_line = y.strip().split('\n')[-1]
        if 'left: ' not in last_line:  # last step
            ans = last_line.lower().replace('answer: ', '')
            # print([value_last_step_prompt.format(input=x, answer=ans)])
            return value_last_step_prompt.format(input=x, answer=ans)
        current_numbers = get_current_numbers(y)
        return value_prompt.format(input=current_numbers)

    @staticmethod
    def validation_outputs_unwrap(x: str, y: str, value_outputs: list) -> float:
        validations = [_.split('\n')[-1] for _ in value_outputs]
        if "invalid" in validations:
            return 0
        return 1

    @staticmethod
    def reflect_prompt_wrap(x: str, y: str, feedback: str) -> str:
        return reflect_prompt.format(input=x, answer=y, feedback=feedback), value_reflect_prompt.format(input=x,
                                                                                                        answer=y,
                                                                                                        feedback=feedback)

    @staticmethod
    def value_outputs_unwrap(x: str, y: str, value_outputs: list) -> float:
        if len(y.strip().split('\n')) == 4 and 'answer' not in y.lower():
            return 0
        value_names = [_.split('\n')[-1].lower() for _ in value_outputs]
        value_map = {'impossible': 0.001, 'likely': 1, 'sure': 20}  # TODO: ad hoc
        value = sum(value * sum(name in value_name for value_name in value_names) for name, value in value_map.items())
        return value
