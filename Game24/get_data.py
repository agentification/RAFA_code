import numpy as np
from plot_utils import data_process
import json

LOG_ROOT = "../log"


def get_curve(data):
    trials = [len(entry['env_info']) + 3 for entry in data]
    hist = {}
    for trial in trials:
        if trial > 20:
            continue
        if trial not in hist:
            hist[trial] = 0

        hist[trial] += 1

    hist_list = [0 for _ in range(21)]
    for key in hist:
        # print(key)
        hist_list[key] = hist[key]

    trails_curve = np.cumsum(hist_list)
    return trails_curve


def get_data(filename):
    with open(f"{LOG_ROOT}/{filename}", "r") as f:
        data = json.load(f)
        trail_curve = get_curve(data)

    return data_process(trail_curve.reshape(-1, 1))