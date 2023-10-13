# Game of 24

Code for the RAFA (Reason for Future, Act for Now) algorithm in Game of 24.

## Environment setup

- Set `OPENAI_API_KEY` environment variable to your OpenAI API key:
```bash
export OPENAI_API_KEY=<your key>
```
## Run the code

### Experiment replication

```
python run.py --backend gpt-4 --task game24 --task_file_path 24.csv --task_start_index 900 --task_end_index 1000 --prompt_sample standard --n_generate_sample 10 --method_generate propose --method_evaluate value --method_select greedy --n_select_sample 1 --n_evaluate_sample 3 --feedback
```

### Params for different method

- baseline ToT method (b=1, b=2)

```
python run.py --backend gpt-4 --task game24 --task_file_path 24.csv --task_start_index 900 --task_end_index 1000 --prompt_sample standard --n_generate_sample 10 --method_generate propose --method_evaluate value --method_select greedy --n_select_sample 1 --n_evaluate_sample 3 --planning tot
```

```
python run.py --backend gpt-4 --task game24 --task_file_path 24.csv --task_start_index 900 --task_end_index 1000 --prompt_sample standard --n_generate_sample 10 --method_generate propose --method_evaluate value --method_select greedy --n_select_sample 2 --n_evaluate_sample 3 --planning tot
```

- baseline Reflexion method

```
python run.py --backend gpt-4 --task game24 --task_file_path 24.csv --task_start_index 900 --task_end_index 1000 --prompt_sample standard --n_generate_sample 10 --method_generate propose --method_evaluate value --method_select greedy --n_select_sample 1 --n_evaluate_sample 3 --planning naive --feedback
```

- RAFA (b=1, b=2)

```
python run.py --backend gpt-4 --task game24 --task_file_path 24.csv --task_start_index 900 --task_end_index 1000 --prompt_sample standard --n_generate_sample 10 --method_generate propose --method_evaluate value --method_select greedy --n_select_sample 1 --n_evaluate_sample 3 --planning tot --feedback
```

```
python run.py --backend gpt-4 --task game24 --task_file_path 24.csv --task_start_index 900 --task_end_index 1000 --prompt_sample standard --n_generate_sample 10 --method_generate propose --method_evaluate value --method_select greedy --n_select_sample 2 --n_evaluate_sample 3 --planning tot --feedback
```


### GPT 3.5
To run gpt-3.5-turbo, just replace `--backend gpt-4` with `--backend gpt-3.5-turbo`. You can use `--backend gpt-3.5-turbo-16k` to avoid context length error if possible.
