import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Function to read the aggregated data
def read_aggregated_data(filepath):
    return pd.read_csv(filepath)

# Function to add bars with error for ansor, our, and roller
def add_bars(ax, ansor_data, our_data, roller_data, index, bar_width):
    # Plot ansor and our bars with error
    for i, row in ansor_data.iterrows():
        # Ansor bars
        ansor_1_mean = row['1_mean_gflops']
        ansor_2_mean = row['2_mean_gflops']
        
        ansor_1_error = (row['1_max_gflops'] - row['1_mean_gflops']) / row['1_mean_gflops']**2
        ansor_2_error = (row['2_max_gflops'] - row['2_mean_gflops']) / row['2_mean_gflops']**2
        
        # Our bars
        our_1_mean = our_data.loc[i, '1_mean_gflops']
        our_2_mean = our_data.loc[i, '2_mean_gflops']
        
        our_1_error = (our_data.loc[i, '1_max_gflops'] - our_data.loc[i, '1_mean_gflops']) / our_data.loc[i, '1_mean_gflops']**2
        our_2_error = (our_data.loc[i, '2_max_gflops'] - our_data.loc[i, '2_mean_gflops']) / our_data.loc[i, '2_mean_gflops']**2
        
        # Plot Ansor bars with hatch patterns
        ax.bar(index[i] - bar_width, ansor_1_mean, bar_width, label='Ansor (1 min)' if i == 0 else '', color='lightblue', capsize=18)
        # ax.bar(index[i] - bar_width, ansor_2_mean - ansor_1_mean, bar_width, yerr=ansor_2_error, label='Ansor (2 mins)' if i == 0 else '', color='blue', bottom=ansor_1_mean, capsize=18)
        ax.bar(index[i] - bar_width, ansor_2_mean - ansor_1_mean, bar_width, label='Ansor (2 mins)' if i == 0 else '', color='blue', bottom=ansor_1_mean, capsize=18)
        
        # Plot Our bars with hatch patterns
        ax.bar(index[i], our_1_mean, bar_width, label='Our (1 min)' if i == 0 else '', color='orange', capsize=18)
        # ax.bar(index[i], our_2_mean - our_1_mean, bar_width, yerr=our_2_error, label='Our (2 mins)' if i == 0 else '', color='red', bottom=our_1_mean, capsize=18)  # Use orange color for 2_mean
        ax.bar(index[i], our_2_mean - our_1_mean, bar_width, label='Our (2 mins)' if i == 0 else '', color='red', bottom=our_1_mean, capsize=18)  # Use orange color for 2_mean
        
        # Roller bar
        if i in roller_data['testcase'].values:
            roller_row = roller_data[roller_data['testcase'] == i]
            roller_perf = roller_row['mean_gflops'].values[0]
            roller_error = (roller_row['max_gflops'].values[0] - roller_row['mean_gflops'].values[0]) / roller_row['mean_gflops'].values[0]**2
            ax.bar(index[i] + bar_width, roller_perf, bar_width, label='Roller Top50' if i == 0 else '', color='green', capsize=18)

    for i, row in ansor_data.iterrows():
        ansor_best_mean = row['best_mean_gflops']
        ax.plot(index[i] - bar_width, ansor_best_mean, 'x', color='black', markersize=5)  # Star for ansor

    for i, row in our_data.iterrows():
        our_best_mean = row['best_mean_gflops']
        ax.plot(index[i], our_best_mean, '*', color='black', markersize=5)  # Star for our


# Function to plot all test cases for a network
def plot_all_testcases(ansor_data, our_data, roller_data, network, data_folder, machine):
    num_testcases = ansor_data.shape[0]
    bar_width = 0.1
    index = np.arange(num_testcases) * bar_width * 4

    fig, ax = plt.subplots(figsize=(num_testcases * 2, 6))
    add_bars(ax, ansor_data, our_data, roller_data, index, bar_width)

    ax.set_xticks(index)
    ax.set_xticklabels(ansor_data['testcase_'])
    ax.set_xlabel('Testcases')
    ax.set_ylabel('Performance (Gflops)')
    ax.set_title(f'Performance Comparison for {network}')
    ax.legend()
    # y-axis start from 0
    ax.set_ylim(bottom=0)
    ax.yaxis("")
    plt.tight_layout()
    plt.savefig(f'{data_folder}/{machine}_{network}.png')

# Read the aggregated data for ansor, our, and roller
data_folders = ['/home/chendi/githdd/plot/data/4090csv', '/home/chendi/githdd/plot/data/3090csv']

for data_folder in data_folders:
    mm_ansor = read_aggregated_data(f'{data_folder}/ansor/mm_aggregated_data.csv')
    mm_our = read_aggregated_data(f'{data_folder}/our/mm_aggregated_data.csv')
    mm_roller = pd.read_csv(f'{data_folder}/roller/mm_top50_summary.csv')

    yolo_ansor = read_aggregated_data(f'{data_folder}/ansor/yolo_aggregated_data.csv')
    yolo_our = read_aggregated_data(f'{data_folder}/our/yolo_aggregated_data.csv')
    yolo_roller = pd.read_csv(f'{data_folder}/roller/yolo_top50_summary.csv')

    resnet_ansor = read_aggregated_data(f'{data_folder}/ansor/resnet_aggregated_data.csv')
    resnet_our = read_aggregated_data(f'{data_folder}/our/resnet_aggregated_data.csv')
    resnet_roller = pd.read_csv(f'{data_folder}/roller/resnet_top50_summary.csv')
    machine = data_folder.split('/')[-1]
    # Plot all testcases for each network
    plot_all_testcases(mm_ansor, mm_our, mm_roller, 'mm', data_folder, machine)
    plot_all_testcases(yolo_ansor, yolo_our, yolo_roller, 'yolo', data_folder, machine)
    plot_all_testcases(resnet_ansor, resnet_our, resnet_roller, 'resnet', data_folder, machine)

