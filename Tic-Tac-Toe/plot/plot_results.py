import numpy as np
import matplotlib
import matplotlib as mpl
import matplotlib.pyplot as plt
from plot_utils import *
from get_data import get_data


logs = ['Base_gpt-4_vs_MPC3_gpt-4_temp0.2', 'Base_gpt-4_vs_MPC4_gpt-4_temp0.2']
labels = [r'$\texttt{RAFA} (B=3)$', r'$\texttt{RAFA} (B=4)$']


config['xlabel'] = 'Episode'
config['ylabel'] = 'Score'
my_cmap = mpl.colormaps['tab20']
plt.rc('text', usetex=True)
plt.rc('text.latex', preamble=r'\usepackage{amsmath}')

plt.title('Tic-Tac-Toe (Player O)', size=40)

fig = matplotlib.pyplot.gcf()
fig.set_size_inches(16, 12)

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_color('black')
ax.spines['bottom'].set_color('black')

plt.tick_params('x', labelsize=40.0)
plt.tick_params('y', labelsize=40.0)
plt.ylim(-0.6, 1.1)
plt.xlim(0, 20)
plt.xlabel(config['xlabel'], {'size': 40.0})
plt.ylabel(config['ylabel'], {'size': 40.0})

ax.xaxis.set_major_locator(ticker.MaxNLocator(6))
ax.yaxis.set_major_locator(ticker.MaxNLocator(6))

for log, label, color in zip(logs, labels, color_list):
    ax.plot(*get_data(log), color=color, linewidth=10, label=label)
    print(get_data(log))

legend()

plt.savefig('experiment.pdf', format="pdf")
