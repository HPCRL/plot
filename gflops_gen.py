import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


flops_map = {
    'mm': [
        67108864,
        4294967296,
        50331648,
        2415919104,
        4294967296,
        2415919104,
    ],
    'yolo': [
        511377408,
        2727346176,
        2727346176,
        303038464,
        2727346176,
        303038464,
        2727346176,
        303038464,
        10909384704,
        2727346176,
        303038464,
    ],
    'resnet': [
        236027904,
        25690112,
        231211008,
        102760448,
        51380224,
        231211008,
        102760448,
        51380224,
        231211008,
        102760448,
        51380224,
        231211008,
        102760448,
    ],
}


# Function to read the aggregated data
def gen_gflops(filepath):
    data  = pd.read_csv(filepath)
    if not 'testcase' in data.columns and not 'testcase_' in data.columns:
        raise Exception(f"no testcase in {filepath}")
    flops = {}
    if 'yolo' in filepath:
        flops = flops_map['yolo']
    elif 'mm' in filepath:
        flops = flops_map['mm']
    elif 'resnet' in filepath:
        flops = flops_map['resnet']
    else:
        raise Exception(f"no flops for {filepath}")
        
    # iterate each row to add gflops column 1_mean_gflpos, 1_min_gflops, 1_max_gflops, 2_mean_gflops, 2_min_gflops, 2_max_gflops, best_mean_gflops, best_min_gflops, best_max_gflops
    for i, row in data.iterrows():
        flops_1_mean = flops[i] / row['1_mean'] / 1e9
        flops_1_min = flops[i] / row['1_min'] / 1e9
        flops_1_max = flops[i] / row['1_max'] / 1e9
        
        flops_2_mean = flops[i] / row['2_mean'] / 1e9
        flops_2_min = flops[i] / row['2_min']  / 1e9   
        flops_2_max = flops[i] / row['2_max'] / 1e9
        
        flops_best_mean = flops[i] / row['best_mean'] / 1e9
        flops_best_min = flops[i] / row['best_min'] / 1e9
        flops_best_max = flops[i] / row['best_max'] / 1e9
        
        # time min should be the max gflops
        data.loc[i, '1_mean_gflops'] = round(flops_1_mean, 3)
        data.loc[i, '1_min_gflops'] =  round(flops_1_max , 3)
        data.loc[i, '1_max_gflops'] =  round(flops_1_min, 3)
        
        data.loc[i, '2_mean_gflops'] =  round(flops_2_mean, 3)
        data.loc[i, '2_min_gflops'] = round(flops_2_max, 3)
        data.loc[i, '2_max_gflops'] = round(flops_2_min, 3)
        
        data.loc[i, 'best_mean_gflops'] =round ( flops_best_mean, 3)
        data.loc[i, 'best_min_gflops'] = round (flops_best_max, 3)
        data.loc[i, 'best_max_gflops'] = round (flops_best_min, 3)
        # print (f"i {i} flops {flops[i]} row {row}")
        # print (f"data = {data}")
        # input()
        
    # write to csv
    data.to_csv(filepath, index=False)
    return data

def gen_gflops_roller(filepath):
    # print (f"gen_gflops_roller {filepath}")
    data  = pd.read_csv(filepath)
    if not 'testcase' in data.columns and not 'testcase_' in data.columns:
        raise Exception(f"no testcase in {filepath}")
    flops = {}
    if 'resnet' in filepath:
        flops = flops_map['resnet']
    elif 'yolo' in filepath:
        flops = flops_map['yolo']
    elif 'mm' in filepath:
        flops = flops_map['mm']
    else:
        raise Exception(f"no flops for {filepath}")
    # gen gflops for mean,min,max flops
    # print (f"len(flops) {len(flops)} data.shape[0] {data.shape[0]}")
    assert len(flops) == data.shape[0]
    for i, row in data.iterrows():
        # print (f"i {i} flops {flops[i]} row {row}")
        mean_flops = flops[i] / row['mean'] / 1e9
        min_flops = flops[i] / row['min'] / 1e9
        max_flops = flops[i] / row['max'] / 1e9
        
        data.loc[i, 'mean_gflops'] = round(mean_flops, 3)
        data.loc[i, 'min_gflops'] =  round(max_flops, 3)
        data.loc[i, 'max_gflops'] =  round(min_flops, 3)
        
    # write to csv
    data.to_csv(filepath, index=False)
    return data


# Read the aggregated data for ansor, our, and roller and calculate gflops
import sys
data_folder = sys.argv[1]
# mm_ansor = gen_gflops(f'{data_folder}/ansor/mm_aggregated_data.csv')
# mm_our = gen_gflops(f'{data_folder}/our/mm_aggregated_data.csv')
# mm_roller = gen_gflops_roller(f'{data_folder}/roller/mm_top50_summary.csv')

# yolo_ansor = gen_gflops(f'{data_folder}/ansor/yolo_aggregated_data.csv')
# yolo_our = gen_gflops(f'{data_folder}/our/yolo_aggregated_data.csv')
# yolo_roller = gen_gflops_roller(f'{data_folder}/roller/yolo_top50_summary.csv')

# resnet_ansor = gen_gflops(f'{data_folder}/ansor/resnet_aggregated_data.csv')
# resnet_our = gen_gflops(f'{data_folder}/our/resnet_aggregated_data.csv')
# resnet_roller = gen_gflops_roller(f'{data_folder}/roller/resnet_top50_summary.csv')


# mm_ansordynamic = gen_gflops(f'{data_folder}/ansordynamic/mm_aggregated_data.csv')
# yolo_ansordynamic = gen_gflops(f'{data_folder}/ansordynamic/yolo_aggregated_data.csv')
# resnet_ansordynamic = gen_gflops(f'{data_folder}/ansordynamic/resnet_aggregated_data.csv')


mm_our = gen_gflops(f'{data_folder}/our/mm_aggregated_data.csv')
yolo_our = gen_gflops(f'{data_folder}/our/yolo_aggregated_data.csv')
resnet_our = gen_gflops(f'{data_folder}/our/resnet_aggregated_data.csv')
# # Plot all testcases for each network
# plot_all_testcases(mm_ansor, mm_our, mm_roller, 'mm')
# plot_all_testcases(yolo_ansor, yolo_our, yolo_roller, 'yolo')
# plot_all_testcases(resnet_ansor, resnet_our, resnet_roller, 'resnet')

