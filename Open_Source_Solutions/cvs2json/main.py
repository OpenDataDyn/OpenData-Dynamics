
import csv
import json
import argparse
import os

def csv_to_json(csv_file_paths, json_file_path, delimiter=',', encoding='utf-8', columns=None, key=None):
    """
    Convert one or more CSV files to a JSON file.
    
    Parameters:
    - csv_file_paths (list of str): Paths to the CSV files to convert.
    - json_file_path (str): Path to the JSON file where the data will be saved.
    - delimiter (str, optional): The delimiter used in the CSV files. Defaults to ','.
    - encoding (str, optional): The encoding used in the CSV files. Defaults to 'utf-8'.
    - columns (list of str, optional): List of columns to include in the JSON output.
    - key (str, optional): The key under which the CSV data will be saved in the JSON file.
    
    Returns:
    - str: A message indicating the success or failure of the operation.
    """
    
    # Existing JSON data
    existing_data = {}
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as json_file:
            existing_data = json.load(json_file)
    
    if key:
        nested_data = existing_data.get(key, [])
    else:
        nested_data = existing_data.get('root', [])
    
    for csv_file_path in csv_file_paths:
        try:
            # Read CSV file
            with open(csv_file_path, 'r', encoding=encoding) as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter=delimiter)
                data = [row for row in csv_reader]
                
                # Filter columns if specified
                if columns:
                    filtered_data = [{col: row.get(col, None) for col in columns} for row in data]
                    data = filtered_data
                
            nested_data.extend(data)
        except Exception as e:
            print(f"An error occurred while converting {csv_file_path}: {e}")
    
    # Update existing JSON data
    if key:
        existing_data[key] = nested_data
    else:
        existing_data['root'] = nested_data
    
    # Write updated data to JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)

    return "CSV files converted and appended to JSON successfully."

# Command-line arguments
parser = argparse.ArgumentParser(description='Convert CSV files to JSON.')
parser.add_argument('--csv_files', type=str, nargs='+', required=True, help='The file paths to the CSV files you want to convert.')
parser.add_argument('--json_file', type=str, required=True, help='The file path where the JSON data will be saved.')
parser.add_argument('--delimiter', type=str, default=',', help='The delimiter used in the CSV files. Optional.')
parser.add_argument('--encoding', type=str, default='utf-8', help='The encoding used in the CSV files. Optional.')
parser.add_argument('--columns', type=str, nargs='*', help='List of columns to include in the JSON. Optional.')
parser.add_argument('--key', type=str, help='The key in the JSON file where the CSV data will be saved. Optional.')
args = parser.parse_args()

message = csv_to_json(args.csv_files, args.json_file, args.delimiter, args.encoding, args.columns, args.key)
print(message)
