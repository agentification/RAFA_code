import numpy as np
import json
from plot_utils import smooth

LOG_ROOT = "output"

reward_func = {'O': 1, 'Tie': 0, 'X': -1}


def get_curve(data):
    return np.mean([reward_func[x] for x in data['winner']])


def get_data(dir, n=12):
    trial_curve = []
    trials = list(range(n))
    for trial in trials:
        with open(f"{LOG_ROOT}/{dir}/{trial}/eval.json", "r") as f:
            data = json.load(f)
        trial_curve.append(get_curve(data))
    return trials, smooth(np.array(trial_curve).reshape(1, -1), 5).reshape(-1)
    