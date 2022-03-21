import pandas as pd
import numpy as np
from pathlib import Path
from tabulate import tabulate
from process_uv_data import get_uv_table
import matplotlib.pyplot as plt


def stem_plot():
    data = get_uv_table(SHOW_ALL=True)[1:]
    fig, ax = plt.subplots()

    #data_a = np.array()
    #data_b = np.array()
    #data_c = np_array()

    (markers, stemlines, baseline) = plt.stem(np.arange(4), [sunscreen[2] for sunscreen in data[:4]])
    plt.setp(markers, markerfacecolor="purple", markeredgecolor="purple")

    (markers, stemlines, baseline) = plt.stem(np.arange(start=5, stop=9), [sunscreen[2] for sunscreen in data[4:8]])
    plt.setp(markers, markerfacecolor="pink", markeredgecolor="pink")

    (markers, stemlines, baseline) = plt.stem(np.arange(start=9, stop=13), [sunscreen[2] for sunscreen in data[8:]])
    plt.setp(markers, markerfacecolor="black", markeredgecolor="black")
    plt.show()

def box_plot():
    data = get_uv_table(SHOW_ALL=True)[1:]
    targets = [sunscreen[2] for sunscreen in data]
    print(targets)
    D = [targets[0:4], targets[4:8], targets[8:]]
    print(D)
    fig, ax = plt.subplots()
    ax.boxplot(D, positions=[2,4,6], widths=1.5, patch_artist=True,
                showmeans=False, showfliers=False,
                medianprops={"color": "white", "linewidth": 0.5},
                boxprops={"facecolor": "C0", "edgecolor": "white",
                          "linewidth": 0.5},
                whiskerprops={"color": "C0", "linewidth": 1.5},
                capprops={"color": "C0", "linewidth": 1.5})
    plt.show()

def bar_plot():
    raw = get_uv_table(SHOW_ALL=True)
    data = raw[1:]
    D = [data[0:4], data[4:8], data[8:]]
    width = 0.4
    labels=['Experiment 1', 'Experiment 2', 'Experiment 3', 'Experiment  4']
    for sunscreen in D:
        fig, axs = plt.subplots(2)
        fig.suptitle("Eucerin Photoaging", fontsize=28)


        #axs[0].bar(np.arange(4) - width/2, [run[2] for run in sunscreen], width, label="UV-A before filter", color="mediumpurple")
        #axs[0].bar(np.arange(4) - width/2, [run[2] for run in sunscreen], width, label="UV-A before filter", color="orange")
        axs[0].bar(np.arange(4) - width/2, [run[2] for run in sunscreen], width, label="UV-A before filter", color="cornflowerblue")

        #axs[0].bar(np.arange(4) + width/2, [run[4] for run in sunscreen], width, label="UV-A after filter", color="indigo")
        #axs[0].bar(np.arange(4) + width/2, [run[4] for run in sunscreen], width, label="UV-A after filter", color="silver")
        axs[0].bar(np.arange(4) + width/2, [run[4] for run in sunscreen], width, label="UV-A after filter", color="lightsteelblue")
        axs[0].set_xticks(np.arange(4), labels)
        axs[0].set_yticks(np.arange(0, 100, 10))
        axs[0].set_title("UV-A measurements")
        axs[0].legend()

        #axs[1].bar(np.arange(4) - width/2, [run[3] for run in sunscreen], width, label="UV-B before filter", color="lightseagreen")
        #axs[1].bar(np.arange(4) - width/2, [run[3] for run in sunscreen], width, label="UV-B before filter", color="limegreen")
        axs[1].bar(np.arange(4) - width/2, [run[3] for run in sunscreen], width, label="UV-B before filter", color="firebrick")

        #axs[1].bar(np.arange(4) + width/2, [run[5] for run in sunscreen], width, label="UV-B after filter", color="silver")
        #axs[1].bar(np.arange(4) + width/2, [run[5] for run in sunscreen], width, label="UV-B after filter", color="forestgreen")
        axs[1].bar(np.arange(4) + width/2, [run[5] for run in sunscreen], width, label="UV-B after filter", color="lightsalmon")
        axs[1].set_xticks(np.arange(4), labels)
        axs[1].set_yticks(np.arange(0, 100, 10))
        plt.xlabel("Time (s)")
        plt.ylabel("UV (relative unit)")
        axs[1].set_title("UV-B measurements")
        axs[1].legend()
        plt.show()

if __name__ == "__main__":
    bar_plot()
    print(tabulate(get_uv_table(SHOW_MINIMAL=True)))
