# BlocksWorld

Code for the RAFA (Reason for Future, Act for Now) algorithm in the BlocksWorld environment.

## Environment setup

- Our experiments are conducted with Vicuna-13B/33B (v1.3). The required packages can be installed by
    ```
    pip install -r requirements.txt
    ```


## Run the code

- To run the RAP experiments, here is a shell script of the script
    ```bash
    CUDA_VISIBLE_DEVICES=0,1,2 nohup python -m torch.distributed.run --master_port 1034 --nproc_per_node 1 run_mcts.py --task mcts --model_name Vicuna --verbose False --data data/blocksworld/step_6.json --max_depth 6 --name m6ct_roll60 --rollouts 60 --model_path lmsys/vicuna-33b-v1.3 --num_gpus 3
    ```

- To run the RAFA experiments, here is a shell script example
    ```bash
    CUDA_VISIBLE_DEVICES=0,1,2 nohup python -m torch.distributed.run --master_port 36977 --nproc_per_node 1 run_rafa_mcts.py --model_name Vicuna --verbose False --data data/blocksworld/step_6.json --max_depth 6 --name rafm_step6_33b_try60 --rollouts 60 --model_path lmsys/vicuna-33b-v1.3 --num_gpus 3
    ```

- For details on the runtime arguments, one can use `python run_rafa_mcts.py --help`.
