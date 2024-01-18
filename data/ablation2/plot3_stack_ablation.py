import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Function to read the aggregated data
def read_aggregated_data(filepath):
    return pd.read_csv(filepath)

# Function to add bars with error for ansor, ansordynamic, and roller
def add_bars(ax, ansor_data, ansordynamic_data, index, bar_width):
    # Plot ansor and ansordynamic bars with error
    for i, row in ansor_data.iterrows():
        # Ansor bars
        ansor_1_mean = 1 / row['1_mean']
        ansor_2_mean = 1 / row['2_mean']
        
        ansor_1_error = (row['1_max'] - row['1_mean']) / row['1_mean']**2
        ansor_2_error = (row['2_max'] - row['2_mean']) / row['2_mean']**2
        
        # ansordynamic bars
        ansordynamic_1_mean = 1 / ansordynamic_data.loc[i, '1_mean']
        ansordynamic_2_mean = 1 / ansordynamic_data.loc[i, '2_mean']
        
        ansordynamic_1_error = (ansordynamic_data.loc[i, '1_max'] - ansordynamic_data.loc[i, '1_mean']) / ansordynamic_data.loc[i, '1_mean']**2
        ansordynamic_2_error = (ansordynamic_data.loc[i, '2_max'] - ansordynamic_data.loc[i, '2_mean']) / ansordynamic_data.loc[i, '2_mean']**2
        
        # Plot Ansor bars with hatch patterns
        ax.bar(index[i] - bar_width, ansor_1_mean, bar_width, label='Ansor (1_mean)' if i == 0 else '', color='lightgreen', hatch="//", capsize=20)
        ax.bar(index[i] - bar_width, ansor_2_mean - ansor_1_mean, bar_width, yerr=ansor_2_error, label='Ansor (2_mean)' if i == 0 else '', color='green', bottom=ansor_1_mean, capsize=20)
        
        # Plot ansordynamic bars with hatch patterns
        ax.bar(index[i], ansordynamic_1_mean, bar_width, label='ansordynamic (1_mean)' if i == 0 else '', color='lightblue', hatch="xx", capsize=20)
        ax.bar(index[i], ansordynamic_2_mean - ansordynamic_1_mean, bar_width, yerr=ansordynamic_2_error, label='ansordynamic (2_mean)' if i == 0 else '', color='blue', bottom=ansordynamic_1_mean, capsize=20)  # Use orange color for 2_mean
        
    for i, row in ansor_data.iterrows():
        ansor_best_mean = 1 / row['best_mean']
        ax.plot(index[i] - bar_width, ansor_best_mean, '*', color='black', markersize=10)  # Star for ansor

    for i, row in ansordynamic_data.iterrows():
        ansordynamic_best_mean = 1 / row['best_mean']
        ax.plot(index[i], ansordynamic_best_mean, '*', color='black', markersize=10)  # Star for ansordynamic




# Function to plot all test cases for a network
def plot_all_testcases(ansor_data, ansordynamic_data, network):
    num_testcases = ansor_data.shape[0]
    bar_width = 0.05
    index = np.arange(num_testcases) * bar_width * 3

    fig, ax = plt.subplots(figsize=(num_testcases * 2, 6))
    add_bars(ax, ansor_data, ansordynamic_data, index, bar_width)

    ax.set_xticks(index)
    ax.set_xticklabels(ansor_data['testcase_'])
    ax.set_xlabel('Testcases')
    ax.set_ylabel('Performance (1/time)')
    ax.set_title(f'Performance Comparison for {network}')
    ax.legend()
    # y-axis start from 0
    ax.set_ylim(bottom=0)
    

    plt.tight_layout()
    

    plt.savefig(f'ablation2{network}.png')

# Read the aggregated data for ansor, ansordynamic, and roller
data_folder = './'

yolo_ansor = read_aggregated_data(f'{data_folder}/ansor/yolo_aggregated_data.csv')
yolo_ansordynamic = read_aggregated_data(f'{data_folder}/ansordynamic/yolo_aggregated_data.csv')
# yolo_roller = pd.read_csv(f'{data_folder}/roller/yolo_top50_summary.csv')

resnet_ansor = read_aggregated_data(f'{data_folder}/ansor/resnet_aggregated_data.csv')
resnet_ansordynamic = read_aggregated_data(f'{data_folder}/ansordynamic/resnet_aggregated_data.csv')
# resnet_roller = pd.read_csv(f'{data_folder}/roller/resnet_top50_summary.csv')

# Plot all testcases for each network
plot_all_testcases(yolo_ansor, yolo_ansordynamic, 'yolo')
plot_all_testcases(resnet_ansor, resnet_ansordynamic, 'resnet')

