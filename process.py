import pandas as pd
import os
import glob
import sys
# Function to read CSV files for a specific network and aggregate them
def read_and_aggregate_csv(network, directory, name):
    print("processing", network, directory, name)
    # Pattern to match the network files
    if network == 'mm':
        pattern = f"{directory}/{name}_run_time[0-9]_summary.csv"  # Matches only MM files
    else:
        pattern = f"{directory}/{name}_run_time*_{network}_summary.csv"

    # Using glob to match all files that fit the pattern
    files = glob.glob(pattern)
    if len(files) == 0:
        raise Exception(f"No files found for {network} in {directory}")
    print("List of files:", files)
    # if len(files) == 0:
    #     if network == 'mm':
    #         pattern = f"{directory}/{name}_run_time[0-9]_summmary.csv"  # Matches only MM files
    #     else:
    #         pattern = f"{directory}/{name}_run_time*_{network}_summmary.csv"
    #     files = glob.glob(pattern)

    # Read and aggregate all files that match the pattern
    aggregated_data = pd.DataFrame()
    for file in files:
        df = pd.read_csv(file)
        # # Recalculate 'best' as the maximum of '1', '2', and 'best'
        # # print (df)
        # df['best'] = df[['1', '2', 'best']].min(axis=1)
        # # print (df)
        aggregated_data = pd.concat([aggregated_data, df])
    
    # Calculate mean, min, and max for '1', '2', and 'best'
    try:
        aggregated_data = aggregated_data.groupby('testcase').agg({'1': ['mean', 'min', 'max'],
                                                               '2': ['mean', 'min', 'max'],
                                                               'best': ['mean', 'min', 'max']}).reset_index()
    except Exception as e:
        print(f"Error in {network} {directory} {name}")
    # Flatten the MultiIndex columns
    aggregated_data.columns = ['_'.join(col).strip() for col in aggregated_data.columns.values]
    
    return aggregated_data

# Directory where the files are located
# directory = [
#     "/home/chendi/githdd/plot/data/processed_ncu/raw3090",
#     "/home/chendi/githdd/plot/data/processed_ncu/raw4090",
# ]
# des_dir ='/home/chendi/githdd/plot/data/4090csv'


directory = sys.argv[1]
des_dir = sys.argv[2]

names = ['our']
# Networks for which the data needs to be aggregated
networks = ['resnet', 'yolo', 'mm']

for name in names:
    # Process the data for each network
    for network in networks:
        machine = directory.split('/')[-1]
        network_data = read_and_aggregate_csv(network, directory, name)
        # Save the aggregated data to a new CSV file
        if not os.path.exists('.tmp'):
            os.makedirs('.tmp')
        
        if not os.path.exists(f'.tmp/{machine}'):
            os.makedirs(f'.tmp/{machine}')
            
        # create new folder
        if not os.path.exists(f'.tmp/{machine}/{name}'):
            os.makedirs(f'.tmp/{machine}/{name}')
        
        # Save the aggregated data to a new CSV file
        output_file = f".tmp/{machine}/{name}/{network}_aggregated_data.csv"
        network_data.to_csv(output_file, index=False)
        print(f"Aggregated data for {network} saved to {output_file}")
        
        # create
        if not os.path.exists(f'{des_dir}/{name}'):
            os.makedirs(f'{des_dir}/{name}')
        # mv from f".tmp/{machine}" to des_dir
        os.system(f"mv .tmp/{machine}/{name}/{network}_aggregated_data.csv {des_dir}/{name}/")
    