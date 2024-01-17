import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# calculate the mean, min, max of each testcase
def read_and_combine_csv(filenames):
    dataframes = [pd.read_csv(filename) for filename in filenames]
    combined_data = pd.concat(dataframes)
    return combined_data.groupby('testcase').agg(['mean', 'min', 'max']).reset_index()

def add_performance_bar(ax, data, index, bar_width, space, label, color, hatch):
    # calculate the total width of all bars and spaces combined to center them
    total_width = (bar_width + space) * len(data['comparison_data']) - space
    offset = 0.4
    
    for i, column in enumerate(time_columns):
        pos = index[i] - offset + (bar_width + space) * data['order']
        mean = data['summary'].loc[data['summary']['testcase'] == data['testcase'], (column, 'mean')]
        if not mean.empty and not mean.isna().values[0]:
            perf = 1 / mean.values[0]
            error = [
                [perf - 1 / data['summary'].loc[data['summary']['testcase'] == data['testcase'], (column, 'max')].values[0]],
                [1 / data['summary'].loc[data['summary']['testcase'] == data['testcase'], (column, 'min')].values[0] - perf]
            ]
            bar = ax.bar(pos, perf, bar_width, label=label if i == 0 else "", color=color, yerr=error, capsize=5)
            bar[0].set_hatch(hatch)  # Set the hatch pattern
import math

def plot_comparison_with_error_bars(comparison_data, time_columns, network):
    num_testcases = max([data['summary']['testcase'].max() for data in comparison_data]) + 1
    num_comparisons = len(comparison_data)
    bar_width = 0.3 / num_comparisons
    space = 0.01

    # Determine the layout of the subplots
    rows = math.ceil(math.sqrt(num_testcases))
    cols = math.ceil(num_testcases / rows)

    # Create a figure to contain all the subplots
    fig, axs = plt.subplots(rows, cols, figsize=(cols * 8, rows * 6), squeeze=False)

    for testcase in range(num_testcases):
        # Calculate the subplot's position (row and column)
        row = testcase // cols
        col = testcase % cols
        ax = axs[row, col]

        index = np.arange(len(time_columns))
        
        for data in comparison_data:
            add_performance_bar(ax, {**data, 'comparison_data': comparison_data, 'testcase': testcase}, index, bar_width, space, data['label'], data['color'], data['hatch'])

        ax.set_xlabel('Wall Time(minutes)')
        ax.set_title(f'{network} Layer{testcase}')
        ax.set_xticks(index)
        ax.set_xticklabels(time_columns)
        ax.yaxis.set_visible(False)
        if testcase == 0:  # Only add legend to the first subplot to avoid repetition
            ax.legend()

    # Adjust layout to prevent overlap
    plt.tight_layout()
    plt.savefig(f'ncu_{network}.png')


for machine in ['3090', '4090']:
    for network in ['resnet', 'yolo']:
        data_folder = f'./data/{machine}csv/'
        ansor_dir_name = "ansor"
        our_dir_name = "our"
        
        if network == 'mm': # mm naming: no network keyword
            # ansor
            ansor_files = [
                f'{data_folder}{ansor_dir_name}_run_time1_summary.csv',
                f'{data_folder}{ansor_dir_name}_run_time2_summary.csv',
                f'{data_folder}{ansor_dir_name}_run_time3_summary.csv'
            ]
            # our
            ourDynamic_files = [
                f'{data_folder}{our_dir_name}_run_time1_summary.csv',
                f'{data_folder}{our_dir_name}_run_time2_summary.csv',
                f'{data_folder}{our_dir_name}_run_time3_summary.csv'
            ]
            # roller 
        else: # solving yolo/resnet
            # ansor
            ansor_files = [
                f'{data_folder}{ansor_dir_name}_run_time1_{network}_summary.csv',
                f'{data_folder}{ansor_dir_name}_run_time2_{network}_summary.csv',
                f'{data_folder}{ansor_dir_name}_run_time3_{network}_summary.csv'
            ]

            # our
            ourDynamic_files = [
                f'{data_folder}{our_dir_name}_run_time1_{network}_summary.csv',
                f'{data_folder}{our_dir_name}_run_time2_{network}_summary.csv',
                f'{data_folder}{our_dir_name}_run_time3_{network}_summary.csv'
            ]
            # roller 

        # Example usage:
        data_ansor = read_and_combine_csv(ansor_files)
        data_ourDynamic = read_and_combine_csv(ourDynamic_files)

        ################# hatch patterns #################
        # / 
        # \\
        # | 
        # - 
        # + 
        # x 
        # o 
        # O 
        # . 
        # * 

        comparison_data = [
            # {
            #     "summary": data_roller,
            #     "label": "roller",
            #     "color": "#023e8a",
            #     "order": 1,
            #     "hatch": "*",
            # },
            {
                "summary": data_ansor,
                "label": "ansor",
                "color": "blue",
                "order": 2,
                "hatch": "//",
            },
            {
                "summary": data_ourDynamic,
                "label": "ourDynamic",
                "color": "red",
                "order": 3,
                "hatch": "\\\\",
            },
        ]
        print(f"ansor: {data_ansor}")
        #time60,time120,time120,time240,time300,time360,time420,time480,time540,time600,time660,time720,time780,time840,time900,time960,time1020,time1080,time1140,time1200
        # time_columns = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11','12','13','14','15','16','17','18','19','20']
        # time_columns = ['1.0', '2.0', '3.0', '4.0', '5.0', '6.0', '7.0', '8.0', '9.0', '10.0', '11.0','12.0','13.0','14.0','15.0']
        # time_columns = ['1.0', '2.0', '3.0', '4.0', '5.0', '6.0', '7.0', '8.0', '9.0', '10.0']
        # time_columns = ['1.0', '2.0', 'best']
        time_columns = ['1', '2', 'best']
        plot_comparison_with_error_bars(comparison_data, time_columns, network)
        # time_columns = ['time60', 'time120', 'time180', 'time300', 'time600', 'time900', 'time1200']
