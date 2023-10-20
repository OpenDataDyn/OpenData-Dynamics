import argparse
import os
import json
import openpyxl

def excel_to_json(excel_file_paths, json_file_path, sheet_name=0, encoding='utf-8', key=None):
    '''
    Convert one or multiple Excel sheets to a JSON file.
    
    If the JSON file already exists, the function appends the new Excel data to it.
    If a key is specified, the new data will be nested under that key in the JSON file.

    Parameters:
    - excel_file_paths (list): A list of paths to the Excel files that need to be converted.
    - json_file_path (str): The path where the JSON file will be saved or updated.
    - sheet_name (str or int, optional): The name or index of the sheet to read. Defaults to the first sheet.
    - encoding (str, optional): The encoding used in the Excel files. Defaults to 'utf-8'.
    - key (str, optional): The key in the JSON file under which the Excel data will be saved.

    Returns:
    - str: A message indicating whether the Excel files were successfully converted and appended to the JSON file.
    '''
    
    # Existing JSON data
    existing_data = {}
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as json_file:
            existing_data = json.load(json_file)
    
    if key:
        nested_data = existing_data.get(key, [])
    else:
        nested_data = existing_data.get('root', [])
    
    for excel_file_path in excel_file_paths:
        try:
            # Read Excel file
            workbook = openpyxl.load_workbook(excel_file_path)
            if isinstance(sheet_name, int):
                sheet = workbook.worksheets[sheet_name]
            else:
                sheet = workbook[sheet_name]
            
            headers = [cell.value for cell in sheet[1]]
            data = []
            for row in sheet.iter_rows(min_row=2, values_only=True):
                data.append({header: value for header, value in zip(headers, row)})
            
            nested_data.extend(data)
        except Exception as e:
            print(f"An error occurred while converting {excel_file_path}: {e}")
    
    # Update existing JSON data
    if key:
        existing_data[key] = nested_data
    else:
        existing_data['root'] = nested_data
    
    # Write updated data to JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)

    return "Excel files converted and appended to JSON successfully."


# Command-line arguments
parser = argparse.ArgumentParser(description='Convert Excel files to JSON.')
parser.add_argument('--excel_files', type=str, nargs='+', required=True, help='The file paths to the Excel files you want to convert.')
parser.add_argument('--json_file', type=str, required=True, help='The file path where the JSON data will be saved.')
parser.add_argument('--sheet_name', type=str, default=0, help='The name or index of the sheet to read. Optional.')
parser.add_argument('--encoding', type=str, default='utf-8', help='The encoding used in the Excel files. Optional.')
parser.add_argument('--key', type=str, help='The key in the JSON file where the Excel data will be saved. Optional.')
args = parser.parse_args()

message = excel_to_json(args.excel_files, args.json_file, args.sheet_name, args.encoding, args.key)
print(message)
