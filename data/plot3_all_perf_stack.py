import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Function to read the aggregated data
def read_aggregated_data(filepath):
    return pd.read_csv(filepath)

# Corrected function to add bars for a single subplot
def add_subplot_bars(ax, testcase_map, index, bar_width, total_bars=3):
    # Calculate the total width of all bars together
    total_width = total_bars * bar_width
    
    # Calculate offset to center the group of bars
    offset = (total_width - bar_width) / 2
    
    for i, (testcase_key, data) in enumerate(testcase_map.items()):
        ansor_data, our_data, roller_data = data
        
        # Calculate each bar's position
        ansor_pos = index[i] - offset
        roller_pos = index[i] - offset + bar_width
        our_pos = index[i] - offset + 2 * bar_width

        # Plot ansor bars
        ax.bar(ansor_pos, ansor_data['1_mean_gflops'], bar_width, label='Ansor (1 min)' if i == 0 else '', color='lightgreen', edgecolor='grey', capsize=5)
        ax.bar(ansor_pos, ansor_data['2_mean_gflops'] - ansor_data['1_mean_gflops'], bar_width, bottom=ansor_data['1_mean_gflops'], label='Ansor (2 mins)' if i == 0 else '', color='green', edgecolor='grey', capsize=5)
        
        # Plot roller bar if data is available
        if roller_data is not None:
            ax.bar(roller_pos, roller_data['mean_gflops'], bar_width, label='Roller Top50' if i == 0 else '', color='purple', edgecolor='grey', capsize=5)
            
        # Plot our bars
        ax.bar(our_pos, our_data['1_mean_gflops'], bar_width, label='Our (1 min)' if i == 0 else '', color='orange', edgecolor='grey', capsize=5)
        ax.bar(our_pos, our_data['2_mean_gflops'] - our_data['1_mean_gflops'], bar_width, bottom=our_data['1_mean_gflops'], label='Our (2 mins)' if i == 0 else '', color='red', edgecolor='grey', capsize=5)
        
        # Plot stars for best_mean_gflops (ansor)
        ansor_best_mean = ansor_data['best_mean_gflops']
        ax.plot(ansor_pos, ansor_best_mean, 'x', color='black', markersize=5)
        
        # Plot stars for best_mean_gflops (our)
        our_best_mean = our_data['best_mean_gflops']
        ax.plot(our_pos, our_best_mean, '*', color='black', markersize=5)

# Function to plot all test cases from all networks in subplots
def plot_all_testcases_in_subplots(data_folders, networks):
    # Maximum number of test cases per subplot
    max_testcases_per_subplot = 16
    bar_width = 0.25
    # Build the testcase map
    testcase_map = {}
    for data_folder in data_folders:
        for network in networks:
            ansor_data = read_aggregated_data(f'{data_folder}/ansor/{network}_aggregated_data.csv')
            our_data = read_aggregated_data(f'{data_folder}/our/{network}_aggregated_data.csv')
            roller_data = pd.read_csv(f'{data_folder}/roller/{network}_top50_summary.csv', index_col='testcase')

            for testcase in ansor_data['testcase_']:
                key = f"{network}{testcase}"
                testcase_map[key] = (
                    ansor_data[ansor_data['testcase_'] == testcase].iloc[0],
                    our_data[our_data['testcase_'] == testcase].iloc[0],
                    roller_data.loc[testcase] if testcase in roller_data.index else None
                )
    
    # Determine how many subplots we need
    num_subplots = int(np.ceil(len(testcase_map) / max_testcases_per_subplot))
    
    # Create subplots
    fig, axs = plt.subplots(num_subplots, 1, figsize=(15, 5 * num_subplots))
    if num_subplots == 1:
        axs = [axs]  # Make sure axs is iterable even when there is only one subplot
    
    # Add bars to each subplot
    for i in range(num_subplots):
        start_idx = i * max_testcases_per_subplot
        end_idx = min(start_idx + max_testcases_per_subplot, len(testcase_map))
        subplot_testcase_map = dict(list(testcase_map.items())[start_idx:end_idx])
        index = np.arange(len(subplot_testcase_map))
        
        add_subplot_bars(axs[i], subplot_testcase_map, index, bar_width)
        axs[i].set_xticks(index)
        axs[i].set_xticklabels(subplot_testcase_map.keys(), rotation=90)
        axs[i].set_ylabel('GFLOPS')
        
        if i == 0:  # Add legend only to the first subplot
            axs[i].legend()

    fig.suptitle('GFLOPS Performance Comparison', fontsize=18)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig('4090_perf.pdf')


# Define data folders and networks
data_folders = ['/home/chendi/githdd/plot/data/4090csv']
networks = ['mm', 'resnet', 'yolo']

# Plot all test cases
plot_all_testcases_in_subplots(data_folders, networks)
