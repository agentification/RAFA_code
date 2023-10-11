import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from plot_utils import *
from get_data import get_data

config['ylim'] = (0., 100.)
config['xlim'] = (0., 20)
config['xlabel'] = 'Steps'
config['ylabel'] = 'Success Rate (%)'
config['smooth_range'] = 1

legends = ["RAFA (b=2)","RAFA (b=1)"]
filenames = ["gpt-4_0.7_propose10_value3_greedy1_start900_end1000_time1692483447.json","gpt-4_0.7_propose10_value3_greedy2_start900_end1000_time1693762595.json"]

datas = [get_data(filename) for filename in filenames]

plot_all(datas, legends, 1)

plt.title(f'Game of 24', size=30)
legend()
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(16, 10)
plt.savefig(f"./game24.pdf", format="pdf")
plt.show()
