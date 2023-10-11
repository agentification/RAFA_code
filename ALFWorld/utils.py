import os
import openai
from tenacity import (
    retry,
    stop_after_attempt, # type: ignore
    wait_random_exponential, # type: ignore
)

from typing import Optional, List, Union


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def get_completion(prompt: Union[str, List[str]], max_tokens: int = 256, stop_strs: Optional[List[str]] = None, is_batched: bool = False) -> Union[str, List[str]]:
    assert (not is_batched and isinstance(prompt, str)) or (is_batched and isinstance(prompt, list))


    response = openai.ChatCompletion.create(
        engine='gpt-4',
        messages=[
            {"role": "user", "content": prompt}],
        temperature=0.0,
        max_tokens=max_tokens,
        top_p=1,
        stop=stop_strs,
    )
    if is_batched:
        res: List[str] = [""] * len(prompt)
        for choice in response.choices:
            res[choice.index] = choice.text
        return res
    #return response.choices[0].text
    return response.choices[0]["message"]["content"].strip()


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def get_completion_gpt3(prompt: Union[str, List[str]], max_tokens: int = 256, stop_strs: Optional[List[str]] = None, is_batched: bool = False) -> Union[str, List[str]]:
    assert (not is_batched and isinstance(prompt, str)) or (is_batched and isinstance(prompt, list))

    response = openai.ChatCompletion.create(
        engine='gpt-35-turbo',
        messages=[
            {"role": "user", "content": prompt}],
        temperature=0.0,
        max_tokens=max_tokens,
        top_p=1,
        stop=stop_strs,
    )
    if is_batched:
        res: List[str] = [""] * len(prompt)
        for choice in response.choices:
            res[choice.index] = choice.text
        return res
    return response.choices[0]["message"]["content"].strip()
