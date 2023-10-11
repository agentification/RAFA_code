import os
import random
import openai
import requests
from tenacity import retry, retry_if_exception_type, wait_random_exponential, stop_after_attempt


class API:
    EXCEPTION_LIST = (
        openai.error.RateLimitError, 
        openai.error.APIConnectionError, 
        openai.error.Timeout,
    )
    NUM_ATTEMPTS = 6
    DEFAULT_API_KEY = os.getenv('OPENAI_API_KEY')
    DEFAULT_API_TYPE = 'open_ai'
    DEFAULT_API_BASE = 'https://api.openai.com/v1'
    MODELS = ['gpt-3.5-turbo', 'gpt-3.5-turbo-instruct', 'gpt-3.5-turbo-16k', 'gpt-4', 'gpt-4-32k']
    PRICE_RATE = {
        'gpt-3.5-turbo': {'prompt_tokens': 0.002, 'completion_tokens': 0.0015},
        'gpt-3.5-turbo-instruct': {'prompt_tokens': 0.002, 'completion_tokens': 0.0015},
        'gpt-3.5-turbo-16k': {'prompt_tokens': 0.004, 'completion_tokens': 0.003},
        'gpt-4': {'prompt_tokens': 0.06, 'completion_tokens': 0.03},
        'gpt-4-32k': {'prompt_tokens': 0.12, 'completion_tokens': 0.06},
    }

    def __init__(self, *api_keys, api_type=None, api_base=None, api_version=None):
        self.api_keys = list(api_keys) or [self.DEFAULT_API_KEY]
        self.api_type = api_type or self.DEFAULT_API_TYPE
        self.api_base = api_base or self.DEFAULT_API_BASE
        self.api_version = api_version
        self.available_models = []
        self.validate()
        self.usage = {model: {'prompt_tokens': 0, 'completion_tokens': 0} for model in self.available_models}
        self.setup()
    
    def setup(self):
        api_key = random.choice(self.api_keys)
        openai.api_key = api_key
        openai.api_type = self.api_type
        openai.api_base = self.api_base
        openai.api_version = self.api_version
        return api_key
    
    def validate(self):
        self.available_models = self.MODELS
        
    @retry(retry=retry_if_exception_type(EXCEPTION_LIST),
           wait=wait_random_exponential(min=1, max=60),
           stop=stop_after_attempt(NUM_ATTEMPTS))
    def completion(self, prompt, **kargs):
        assert isinstance(prompt, str), 'Completion does NOT support dialogue'
        responses = openai.Completion.create(prompt=prompt, **kargs)
        texts = [response.text for response in responses.choices]
        return texts, responses.usage, responses
    
    @retry(retry=retry_if_exception_type(EXCEPTION_LIST),
           wait=wait_random_exponential(min=1, max=60),
           stop=stop_after_attempt(NUM_ATTEMPTS))
    def chat_completion(self, messages, **kargs):
        responses = openai.ChatCompletion.create(messages=messages, **kargs)
        contents = [response.message.content for response in responses.choices]
        return contents, responses.usage, responses

    def gpt(self, query, model='gpt-4', **kargs):
        assert model in self.available_models, f'{model} is not in the available models {self.available_models}.'
        key = self.setup()
        if self.api_type == 'azure':
            kargs['engine'] = model.replace('.', '')
        else:
            kargs['model'] = model

        while True:
            try:
                if 'turbo-instruct' in model:
                    responses, usage, _ = self.completion(query, **kargs)
                    break
                else:
                    if isinstance(query, str):
                        messages = [{'role': 'user', 'content': query}]
                    elif isinstance(query, list):
                        messages = query
                    else:
                        raise TypeError(f'Your query should be either dialogues (list) or a prompt (str): {query}')
                    responses, usage, _ = self.chat_completion(messages, **kargs)
                    break
            except openai.error.APIError:
                self.api_keys.remove(key)
            
        # log completion tokens
        self.usage[model]['prompt_tokens'] += usage.prompt_tokens
        if 'completion_tokens' in usage:
            self.usage[model]['completion_tokens'] += usage.completion_tokens
        
        return responses
        
    def gpt_usage(self):
        usage = {}
        for model in self.available_models:
            if sum(self.usage[model].values()) > 0:
                usage[model] = sum(self.usage[model][key] * self.PRICE_RATE[model][key] 
                                   for key in self.usage[model]) / 1000
        return usage
