import os
import csv
import json

# get list of exe_time, each[r][0][0] from json file
def get_exe_time_list_from_json(json_path):
    # get real file name 
    foldname = os.path.realpath(json_path).split("/")[-3]
    # print(f"foldname: {foldname}")
    # exit()
    # key = "result" if "tvm" in foldname else "r"
    
    if "tvm" in foldname or "drop" in foldname:
        key = "result"
    else:
        key = "r"
    
    exe_time_list = []
    with open(json_path, "r") as f:
        for line in f:
            if line:
                try:
                    data = json.loads(line)
                    time_value = data.get(key)
                    if time_value:
                        exe_time_list.append(time_value[0][0])
                    else:
                        exe_time_list.append(1e+10)
                        print(f"Warning: '{key}' key not found or time_value is None. for config {line}")
                        # print(f"foldname: {foldname}, key = {key}")
                        # exit()
                except json.JSONDecodeError:
                    # Attempt to fix and decode again
                    line = re.sub(r', "s".*', '', line)+'}'
                    # print(f"Error decoding JSON in line: {line}")
                    try: 
                        data = json.loads(line)
                        time_value = data.get(key)
                    except json.JSONDecodeError:
                        print(f"Error decoding JSON in line: {line}, file: {json_path}")
                        exit()
                    if time_value:
                        exe_time_list.append(time_value[0][0])
                    else:
                        exe_time_list.append(1e+10)
                        print(f"Error: '{key}' key not found or time_value is None. for config {line}")
            else:
                print("Error: file is empty.")
    return exe_time_list

# get corresponding num_configs for elapsed_time
def get_num_configs(csv_file, elapsed_time):
    with open(csv_file, 'r', newline='') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row['elapsed_time'] == str(elapsed_time):
                print("give benifits")
                return int(row['num_configs'])+64
    return None  # return None means no num_configs found


# find at most 5 second before elapsed_time
def find_at_most_5s_before_elapsed_time(csv_file, elapsed_time):
    for time in range(elapsed_time, elapsed_time + 5):
        num_configs = get_num_configs(csv_file, time)
        if num_configs is not None:
            return num_configs
    return 0  # return 0 means no num_configs found

def find_previous_num_configs(csv_file, elapsed_time):
    for time in range(elapsed_time - 1, 0, -1):
        num_configs = get_num_configs(csv_file, time)
        if num_configs is not None:
            return num_configs
    return 0  # return 0 means no num_configs found

import re

# parse file_name to get testcase number
def get_testcase_number(file_name):
    match = re.search(r'testCase_(\d+)', file_name)
    if match:
        return int(match.group(1))
    return 0


def create_summary_csv(input_directory, summary_csv_dir, elapsed_times):
    for root, _, files in os.walk(input_directory):
        if not any(os.path.isdir(os.path.join(root, d)) for d in _):
            # deepest directory
            folder_path = os.path.relpath(root, input_directory)
            folder_name = folder_path.replace("/", "_")
            csv_file_name = folder_name + "_summary.csv"
            summary_csv_path = os.path.join(summary_csv_dir, csv_file_name)


            summary_data = []

            for file_name in files:
                if file_name.endswith('.json'):
                    json_file = os.path.join(root, file_name)
                    
                    csv_file = os.path.splitext(json_file)[0] + '.csv'
                    if "xcuda" in csv_file:
                        csv_file = csv_file.replace("xcuda", "cuda")

                    row_data = {'testcase': get_testcase_number(file_name)}
                    exe_time_list = get_exe_time_list_from_json(json_file)
                    best_time = min(exe_time_list)

                    for elapsed_time in elapsed_times:
                        num_configs = get_num_configs(csv_file, elapsed_time)
                        if num_configs is None:
                            num_configs = find_at_most_5s_before_elapsed_time(csv_file, elapsed_time)
                        min_exe_times = exe_time_list[:num_configs]
                        try:
                            row_data[f'{int(elapsed_time/60)}'] = min(min_exe_times)
                        except ValueError:
                            row_data[f'{int(elapsed_time/60)}'] = None

                    row_data['best'] = best_time
                    summary_data.append(row_data)

            # sort by testcase number
            summary_data.sort(key=lambda x: x['testcase'])

            with open(summary_csv_path, 'w', newline='') as summary_csv:
                fieldnames = ['testcase'] + [f'{int(elapsed_time/60)}' for elapsed_time in elapsed_times] + ['best']
                writer = csv.DictWriter(summary_csv, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(summary_data)

if __name__ == "__main__":
    # input_directory = "./data/4090/4090_ansor"
    input_directory = "/home/chendi/githdd/plot/data/ablation2"
    summary_csv_dir = input_directory
    elapsed_times = [60, 2*60]
    create_summary_csv(input_directory, summary_csv_dir, elapsed_times)