import os
import openai
from tenacity import retry, retry_if_exception_type, wait_random_exponential, stop_after_attempt
from tenacity import wait_fixed

completion_tokens = prompt_tokens = 0
openai.api_key = os.getenv("OPENAI_API_KEY", "")


@retry(retry=retry_if_exception_type(openai.error.OpenAIError), 
       wait=wait_random_exponential(min=1, max=60), 
       stop=stop_after_attempt(100))
def completions_with_backoff(**kwargs):
    if "prompt" in kwargs:
        return openai.Completion.create(**kwargs)
    else:
        assert "messages" in kwargs, "Either prompt or messages must be provided"
        return openai.ChatCompletion.create(**kwargs)


def gpt_with_history(prompt, history, model="gpt-4", temperature=0.7, max_tokens=1000, n=1, stop=None) -> list:
    messages = []
    for h in history:
        if 'answer' in h:
            messages.extend([{"role": "assistant", "content": h["answer"]}])
        if 'feedback' in h:
            messages.extend([{"role": "user", "content": h["feedback"]}])
    messages.append({"role": "user", "content": prompt})

    response = chatgpt(messages, model=model, temperature=temperature, max_tokens=max_tokens, n=n, stop=stop)
    return response

def gpt(prompt, model="gpt-4", temperature=0.7, max_tokens=1000, n=1, stop=None) -> list:
    messages = [{"role": "user", "content": prompt}]
    return chatgpt(messages, model=model, temperature=temperature, max_tokens=max_tokens, n=n, stop=stop)


def chatgpt(messages, model="gpt-4", temperature=0.7, max_tokens=1000, n=1, stop=None) -> list:
    global completion_tokens, prompt_tokens
    outputs = []
    while n > 0:
        cnt = min(n, 20)
        n -= cnt
        if "davinci" in model:
            contents = [m["content"] for m in messages]
            prompt = "\n".join(contents)
            if API == 'us':
                res = completions_with_backoff(
                    prompt=prompt, model=model, temperature=temperature, 
                    max_tokens=max_tokens, n=cnt, stop=stop)
            else:
                res = completions_with_backoff(
                    prompt=prompt, engine=model, temperature=temperature, 
                    max_tokens=max_tokens, n=cnt, stop=stop)

            outputs.extend([choice["text"] for choice in res["choices"]])
        else:
            res = completions_with_backoff(model=model, messages=messages, temperature=temperature, max_tokens=max_tokens,
                                       n=cnt, stop=stop)
            outputs.extend([choice["message"]["content"] for choice in res["choices"]])
        # log completion tokens
        completion_tokens += res["usage"]["completion_tokens"]
        prompt_tokens += res["usage"]["prompt_tokens"]
    return outputs


def gpt_usage(backend="gpt-4"):
    global completion_tokens, prompt_tokens
    if backend == "gpt-4":
        cost = completion_tokens / 1000 * 0.06 + prompt_tokens / 1000 * 0.03
    elif backend == "gpt-3.5-turbo":
        cost = completion_tokens / 1000 * 0.002 + prompt_tokens / 1000 * 0.0015
    else:
        cost = completion_tokens / 1000 * 0.02 + prompt_tokens / 1000 * 0.02
    return {"completion_tokens": completion_tokens, "prompt_tokens": prompt_tokens, "cost": cost}


class Agent:
    def __init__(self):
        pass

    def act(self, env, obs):
        raise NotImplementedError
