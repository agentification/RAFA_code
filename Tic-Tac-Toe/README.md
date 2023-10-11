# Tic-Tac-Toe

Code for the RAFA (Reason for Future, Act for Now) algorithm in Tic-Tac-Toe.

## Environment setup

- Set `OPENAI_API_KEY` environment variable to your OpenAI API key:
```bash
export OPENAI_API_KEY=<your key>
```

## Run the code

### Experiment replication

```
python run.py --X gpt-4 --O gpt-4 --O_MPC 3 --num_train_epochs 12 --num_eval_epochs 10
```

### Parameters

```
--X, --O: the backend model for X player and O player (default: gpt-3.5-turbo-16k)
--X_MPC, --O_MPC: how many actions to propose for X player and O player (default: 1, just base model without MPC)
--temperature: temperature for gpt (default: 0.2)
--eval_freq: evaluation frequency (default: 1)
--num_train_epochs: number of epochs for training (default: 1)
--num_eval_epochs: number of epochs for evaluating (default: 1)
--verbose: auxiliary outputs (default: 1)
```
