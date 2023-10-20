
import argparse
import os
import json
import xml.etree.ElementTree as ET

def xml_to_json(xml_file_paths, json_file_path, encoding='utf-8', key=None):
    """
    Convert one or multiple XML files to a JSON file.
    
    If the JSON file already exists, the function appends the new XML data to it.
    If a key is specified, the new data will be nested under that key in the JSON file.

    Parameters:
    - xml_file_paths (list): A list of paths to the XML files that need to be converted.
    - json_file_path (str): The path where the JSON file will be saved or updated.
    - encoding (str, optional): The encoding used in the XML files. Defaults to 'utf-8'.
    - key (str, optional): The key in the JSON file under which the XML data will be saved.

    Returns:
    - str: A message indicating whether the XML files were successfully converted and appended to the JSON file.
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
    
    for xml_file_path in xml_file_paths:
        try:
            # Read XML file
            tree = ET.parse(xml_file_path)
            root = tree.getroot()
            data = {}
            for elem in root:
                data[elem.tag] = elem.text
                
            nested_data.append(data)
        except Exception as e:
            print(f"An error occurred while converting {xml_file_path}: {e}")
    
    # Update existing JSON data
    if key:
        existing_data[key] = nested_data
    else:
        existing_data['root'] = nested_data
    
    # Write updated data to JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)

    return "XML files converted and appended to JSON successfully."

# Command-line arguments
parser = argparse.ArgumentParser(description='Convert XML files to JSON.')
parser.add_argument('--xml_files', type=str, nargs='+', required=True, help='The file paths to the XML files you want to convert.')
parser.add_argument('--json_file', type=str, required=True, help='The file path where the JSON data will be saved.')
parser.add_argument('--encoding', type=str, default='utf-8', help='The encoding used in the XML files. Optional.')
parser.add_argument('--key', type=str, help='The key in the JSON file where the XML data will be saved. Optional.')
args = parser.parse_args()

message = xml_to_json(args.xml_files, args.json_file, args.encoding, args.key)
print(message)
