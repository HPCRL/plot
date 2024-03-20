import pandas as pd
import glob
import os
import sys

# Define the function to read and process files
def read_and_process_files(directory, network):
    # Define patterns for different file types
    pattern_top10 = os.path.join(directory, f'run_time_*_performance_{network}_top10.csv')
    pattern_top50 = os.path.join(directory, f'run_time_*_performance_{network}_top50.csv')
    
    # Read and process top10 files
    column_name = 'top10'
    top10_df = read_and_process_file(pattern_top10, column_name)
    
    # Read and process top50 files
    column_name = 'top50'
    top50_df = read_and_process_file(pattern_top50, column_name)
    
    # Merge dataframes on 'testcase'
    merged_df = pd.merge(top10_df, top50_df, on='testcase', suffixes=('_top10', '_top50'))
    
    return merged_df

# Define the function to read and process a single file
def read_and_process_file(file_pattern, column_name):
    files = glob.glob(file_pattern)
    
    # Return an empty DataFrame if no files are found
    if not files:
        print(f"No files found for pattern: {file_pattern}")
        return pd.DataFrame()
    
    # Read each file and select relevant columns
    dataframes = []
    for f in files:
        df = pd.read_csv(f)
        
        # Check if 'testcase' column is present
        if 'testcase' not in df.columns:
            print(f"'testcase' column not found in file: {f}")
            print(f"Columns found: {df.columns}")
            continue  # Skip files without 'testcase'
        
        if column_name not in df.columns:
            print(f"'{column_name}' column not found in file: {f}")
            continue  # Skip files without the specified column_name
        
        dataframes.append(df[['testcase', column_name]])
    
    # Concatenate all dataframes
    combined_data = pd.concat(dataframes)
    
    # Group by testcase and calculate mean, min, and max
    summary_stats = combined_data.groupby('testcase')[column_name].agg(['mean', 'min', 'max']).reset_index()
    
    return summary_stats


# Define the directory and column to process
directory = '/home/chendi/githdd/plot/data/processed_ncu/raw3090'
# directory = sys.argv[1]
networks = ['mm', 'resnet', 'yolo']
name = 'roller'
# Process files and save the summaries for each network
for network in networks:
    summary_stats = read_and_process_files(directory, network)
    if not os.path.exists('__output'):
        os.makedirs('__output')
    
    # create new folder
    if not os.path.exists(f'__output/{name}'):
        os.makedirs(f'__output/{name}')
        
    output_file = f"__output/{name}/{network}_aggregated_data.csv"
    summary_stats.to_csv(output_file, index=False)
    print(f"Summary statistics saved to {output_file}")