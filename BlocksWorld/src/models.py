from abc import ABC, abstractmethod

import time

from typing import List, Tuple

import math

import uuid

import torch

import openai
from statistics import mean
from tenacity import retry, stop_after_attempt, retry_if_not_exception_type

from llama import LLaMA

from fastchat.model import load_model


class FakeTokenizer:
    def encode(self, s: str="", bos=False, eos=False):
        return [[]]


class QueryLM(ABC):
    @abstractmethod
    def query_LM(self, prompt, **gen_kwargs):
        pass

    @abstractmethod
    def query_next_token(self, prompt: list[str]):
        pass


class QueryHfModel(QueryLM):
    # This is not well-tested. Please use LLaMA if possible.
    def query_next_token(self, prompt: list[str]):
        raise NotImplementedError

    def __init__(self, model, tokenizer, max_response_length, device):
        self.model = model
        self.tokenizer = tokenizer
        self.device = device
        self.n_examples = 1
        self.max_response_length = max_response_length

    def query_LM(self, prompt, **gen_kwargs):
        with torch.no_grad():
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
            # print("input length", len(inputs))
            # Generate
            generate_ids = self.model.generate(inputs.input_ids, max_new_tokens=self.max_response_length, **gen_kwargs)
            text = self.tokenizer.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=True)
        return text


class QueryLlama(QueryLM):
    def __init__(self, llamamodel: LLaMA, max_response_length, log_file) -> None:
        self.llamamodel = llamamodel
        self.tokenizer = self.llamamodel.tokenizer
        self.max_response_length = max_response_length
        self.log_file = log_file
        self.max_batch_size = llamamodel.model.params.max_batch_size
        self.yes_no = self.tokenizer.encode('Yes No', bos=False, eos=False)

    def query_LM(self, prompt, eos_token_id, num_return_sequences=1, do_sample=True, temperature=0.8):
        temperature = temperature if do_sample else 0
        all_results = []
        for start in range(0, num_return_sequences, self.max_batch_size):
            end = min(start + self.max_batch_size, num_return_sequences)
            results = self.llamamodel.generate([prompt] * (end - start), max_gen_len=self.max_response_length, temperature=temperature, eos_token_id=eos_token_id)
            all_results.extend(results)
        if self.log_file:
            with open(self.log_file, "a") as f:
                f.write("="*50+"\n")
                f.write(prompt + "\n")
                for result in all_results:
                    f.write("-"*50+"\n")
                    f.write(result.replace(prompt, "") + "\n")
        return all_results

    @torch.no_grad()
    def query_next_token(self, prompts):
        if isinstance(prompts, str):
            prompts = [prompts]
        ret = []
        for prompt in prompts:
            tokens = self.tokenizer.encode(prompt, bos=True, eos=False)
            tokens = torch.tensor([tokens]).cuda().long()
            output, h = self.llamamodel.model.forward(tokens, start_pos=0)
            ret.append(output)
        outputs = torch.cat(ret, dim=0)
        filtered = outputs[:, self.yes_no]
        dist = torch.softmax(filtered, dim=-1)
        return dist


class QueryVicuna(QueryLM):
    def __init__(self,
                 model_path='lmsys/vicuna-7b-v1.3',
                 num_gpus=1,
                 repetition_penalty=0.5,
                 max_new_tokens=300) -> None:
        self.llamamodel, self.tokenizer = load_model(
            model_path=model_path,
            device='cuda',
            num_gpus=num_gpus,
            max_gpu_memory='40GiB',
        )
        self.eos_token_id = self.tokenizer.encode('\n', bos=False, eos=False)[-1]
        self.repetition_penalty = repetition_penalty
        self.max_new_tokens = max_new_tokens

    @torch.inference_mode()
    def query_LM(self, prompt: str, do_sample: bool=False, temperature: float=0.8) -> str:
        inputs = self.tokenizer([prompt])
        inputs = {k: torch.tensor(v).cuda() for k, v in inputs.items()}
        output_ids = self.llamamodel.generate(
            **inputs,
            do_sample=do_sample,
            temperature=temperature,
            repetition_penalty=self.repetition_penalty,
            max_new_tokens=self.max_new_tokens,
            eos_token_id=self.tokenizer.encode('\n', bos=False, eos=False)[-1]
        )
        output_ids = output_ids[0][len(inputs["input_ids"][0]) :]
        response = self.tokenizer.decode(output_ids)
        return response

    def query_next_token(self):
        raise NotImplementedError
    
    @torch.no_grad()
    def get_ll(
        self,
        prefix: str,
        prompts: List[str],
    ) -> List[str]:
        bsz = len(prompts)
        prefix_tokens = self.tokenizer(prefix, return_tensors="pt")
        prompts_tokens = [self.tokenizer(x, return_tensors="pt") for x in prompts]
        max_prompt_size = max([len(t.input_ids[0]) for t in prompts_tokens])
        total_len = max_prompt_size
        tokens = torch.full((bsz, total_len), self.eos_token_id).cuda().long()

        logits = []
        for k, t in enumerate(prompts_tokens):
            tokens[k, : len(t.input_ids[0])] = torch.tensor(t.input_ids)[:self.tokenizer.model_max_length].long()
            logits.append(self.llamamodel(tokens[k:k+1, :].to(self.llamamodel.device)).logits)

    #   logits = self.model(tokens.to(self.model.device)).logits
        logits = torch.cat(logits, dim=0)
        acc_probs = torch.zeros(bsz).to(self.llamamodel.device)
        for i in range(len(prefix_tokens.input_ids[0]), max_prompt_size):
            probs = torch.softmax(logits[:, i - 1, :], dim=-1)
            for j in range(bsz):    
                if tokens[j, i] != self.eos_token_id:
                    acc_probs[j] += torch.log(probs[j, tokens[j, i]])

        return acc_probs.cpu().numpy()


class QueryChatGPT(QueryLM):
    def __init__(self, model_path='text-davinci-003') -> None:
        self.tokenizer = FakeTokenizer()
        self.engine = model_path
        with open('data/openai_api_key', 'r') as f:
            openai.api_key = f.read().strip('\n')

    def query_next_token(self, prompt: list[str]):
        raise NotImplementedError

    def query_LM(self, prompt: str, max_retries: int=5, retry_delay: int=5):
        for attempt in range(max_retries):
            try:
                response = openai.Completion.create(
                    engine=self.engine,
                    prompt=prompt,
                    logprobs=0,
                    temperature=0,
                    max_tokens=150,
                    top_p=0.8,
                    frequency_penalty=0.0,
                    presence_penalty=0.0,
                    stop=["\n"],
                )
                return response.choices[0].text.strip()
            
            except openai.error.OpenAIError as e:
                # Handle rate limit errors
                if 'rate limit' in str(e).lower():
                    print(f"Rate limit hit. Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    continue
                
                # Handle other API errors
                print(f"API Error: {e}. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)

        # If the loop completes, we've exceeded our retries
        raise Exception("Failed to get completion after multiple attempts.")

    def smp_get_ll(self, prompt: str, completions: List[str]) -> List[float]:
        @retry(
            stop=stop_after_attempt(10),
            retry=retry_if_not_exception_type((ValueError, OSError))
        )
        def smp_api(prompt, completion):
            return openai.Completion.create(
                engine=self.engine,
                prompt=prompt,
                max_tokens=len(completion.split()),  # Only predict as many tokens as are in the completion
                n=1,  # We only want one prediction
                logprobs=100,  # This gets the top 100 token log probabilities; adjust as needed
                stop=None  # We don't want it to stop early; we want the full token prediction
            )

        log_probs = []
        for completion in completions:
            response = smp_api(prompt, completion)
            tokens = response.choices[0]['logprobs']['tokens']
            token_logprobs = response.choices[0]['logprobs']['token_logprobs']
            # If the completion has multiple tokens, make sure they are all in the tokens returned by the API
            # for token in completion.split():
            #     if token not in tokens:
            #         print(f"WARNING: Token not in predicted tokens for prompt")
            # Calculate the total log probability for the given completion
            a_logprob = sum(token_logprobs[:len(completion.split())])
            # Collect the log probs
            log_probs.append(a_logprob)

        return log_probs
