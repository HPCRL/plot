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
        our_pos = index[i] - offset + bar_width
        roller_pos = index[i] - offset + 2 * bar_width

        ansor_2_error = (ansor_data['2_max_gflops'] - ansor_data['2_min_gflops']) / 2
        our_2_error = (our_data['2_max_gflops'] - our_data['2_min_gflops']) / 2

        # Plot ansor bars
        ax.bar(ansor_pos, ansor_data['1_mean_gflops'], bar_width, 
            label='Ansor (1 min)' if i == 0 else '', color='lightgreen', edgecolor='grey', capsize=5)
        ax.bar(ansor_pos, ansor_data['2_mean_gflops'] - ansor_data['1_mean_gflops'], bar_width,
            bottom=ansor_data['1_mean_gflops'], yerr=ansor_2_error, 
            label='Ansor (2 mins)' if i == 0 else '', color='green', edgecolor='grey', capsize=5)

        # Plot our bars
        ax.bar(our_pos, our_data['1_mean_gflops'], bar_width, 
            label='Ansor-AF-DS (1 min)' if i == 0 else '', color='yellow', edgecolor='grey', capsize=5)
        ax.bar(our_pos, our_data['2_mean_gflops'] - our_data['1_mean_gflops'], bar_width,
            bottom=our_data['1_mean_gflops'], yerr=our_2_error, 
            label='Ansor-AF-DS (2 mins)' if i == 0 else '', color='orange', edgecolor='grey', capsize=5)
        # Plot stars for best_mean_gflops (ansor)
        ansor_best_mean = ansor_data['best_mean_gflops']
        ax.plot(ansor_pos, ansor_best_mean, 'x', color='black', markersize=9)
        
        # Plot stars for best_mean_gflops (our)
        our_best_mean = our_data['best_mean_gflops']
        ax.plot(our_pos, our_best_mean, '*', color='black', markersize=9)
        
        # Plot roller bar if data is available
        if roller_data is not None:
            ax.bar(roller_pos, roller_data['mean_gflops'], bar_width, label='Roller Top50' if i == 0 else '', color='purple', edgecolor='grey', capsize=5)


network_mapping = {
    'mm': 'M',
    'resnet': 'R',
    'yolo': 'Y'
}

# yolo_mapping = {
#     'yolo0': 'Y0',
#     'yolo1': 'Y2',
#     'yolo2': 'Y4',
#     'yolo3': 'Y5',
#     'yolo4': 'Y8',
#     'yolo5': 'Y9',
#     'yolo6': 'Y12',
#     'yolo7': 'Y13',
#     'yolo8': 'Y14',
#     'yolo9': 'Y18',
#     'yolo10': 'Y19'
# }

# Function to plot all test cases from all networks in subplots
def plot_all_testcases_in_subplots(data_folders, networks):
    # Maximum number of test cases per subplot
    max_testcases_per_subplot = 17
    bar_width = 0.25
    # Build the testcase map
    testcase_map = {}
    print(f"processing data_folders = {data_folders}")
    for data_folder in data_folders:
        for network in networks:
            ansor_data = read_aggregated_data(f'{data_folder}/ansor/{network}_aggregated_data.csv')
            our_data = read_aggregated_data(f'{data_folder}/our/{network}_aggregated_data.csv')
            roller_data = pd.read_csv(f'{data_folder}/roller/{network}_top50_summary.csv', index_col='testcase')

            for testcase in ansor_data['testcase_']:
                key = f"{network}{testcase}"
                # if key in yolo_mapping:
                #     # change to 
                #     key = yolo_mapping[key]
                # else:
                #     key = key.replace(network, network_mapping[network])
                key = key.replace(network, network_mapping[network])
                print(key)
                testcase_map[key] = (
                    ansor_data[ansor_data['testcase_'] == testcase].iloc[0],
                    our_data[our_data['testcase_'] == testcase].iloc[0],
                    roller_data.loc[testcase] if testcase in roller_data.index else None
                )
    
    # Determine how many subplots we need
    num_subplots = int(np.ceil(len(testcase_map) / max_testcases_per_subplot))
    
    # Specify the relative heights of each subplot
    height_ratios = [6, 4]  # Adjust the values based on your preference

    # Create subplots with specified heights
    fig, axs = plt.subplots(num_subplots, 1, figsize=(15, sum(height_ratios)), gridspec_kw={'height_ratios': height_ratios})

    if num_subplots == 1:
        axs = [axs]  # Make sure axs is iterable even when there is only one subplot
    
    # Add bars to each subplot
    for i in range(num_subplots):
        start_idx = i * max_testcases_per_subplot
        end_idx = min(start_idx + max_testcases_per_subplot, len(testcase_map))
        subplot_testcase_map = dict(list(testcase_map.items())[start_idx:end_idx])
        index = np.arange(len(subplot_testcase_map))
        
        add_subplot_bars(axs[i], subplot_testcase_map, index, bar_width)
        if i == 0:
            middle_bar_index = 5.5
            axs[i].axvline(middle_bar_index, color='grey', linestyle='--')

        axs[i].set_xticks(index)
        print(subplot_testcase_map.keys())
        axs[i].set_xticklabels(subplot_testcase_map.keys(), rotation=0, fontsize=15)
        axs[i].tick_params(axis='y', labelsize=15)
        axs[i].set_ylabel('GFLOPS', fontsize=20)
        # set front size of ylabel
        axs[i].yaxis.label.set_size(20)
        # if i == 0:  # 只在第一个子图中添加图例
        #     axs[i].legend(loc='upper right', bbox_to_anchor=(1, 1), fontsize=16, prop={'size': 15}, framealpha=1, facecolor='white', edgecolor='black', ncol=3)


    # # plt.xticks(fontsize=15)
    # plt.yticks(fontsize=20)

    # legend = plt.legend(loc='upper center', bbox_to_anchor=(0.12, 1), fontsize=18, prop={'size': 20})
    # legend.get_frame().set_linewidth(2)

    # fig.suptitle('GFLOPS Performance Comparison', fontsize=18)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    machine = data_folders[0].split('/')[-1].split('csv')[0]
    plt.savefig(f'{machine}_perf.pdf')


# Define data folders and networks
# data_folders = ['/home/chendi/githdd/plot/data/4090csv', '/home/chendi/githdd/plot/data/3090csv']
data_folders = ['/home/chendi/githdd/plot/data/4090csv']
data_folders = ['/home/chendi/githdd/plot/data/3090csv']
networks = ['mm', 'yolo', 'resnet']

for dir in data_folders:
    data_folder = []
    data_folder.append(dir)
    # Plot all test cases
    plot_all_testcases_in_subplots(data_folder, networks)
