import time
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def time_complexity_visualizer(algorithm, n_min, n_max, n_step, algo_name=""):
    times = []
    input_sizes = list(range(n_min, n_max + n_step, n_step))

    fig, ax = plt.subplots()
    ax.set_xlabel('Input size')
    ax.set_ylabel('Running time (seconds)')
    title = 'Algorithm time complexity visualisation'
    if algo_name:
        title += f' - {algo_name}'
    ax.set_title(title)

    for n in input_sizes:
        start_time = time.time()
        algorithm(n)
        end_time = time.time()
        times.append(end_time - start_time)

    ax.plot(input_sizes, times, 'o-')
    ax.relim()
    ax.autoscale_view()

    return fig, input_sizes, times
