import base64
import argparse
import os
import json

def convert_file_to_base64(file_path):
    """
    Convert a file to a Base64 string.

    Parameters:
    - file_path (str): The file path to the file you want to convert.

    Returns:
    - str: The Base64 encoded string of the file or an error message.
    """
    try:
        with open(file_path, "rb") as file:
            file_data = file.read()
            base64_encoded = base64.b64encode(file_data).decode("utf-8")
        return base64_encoded
    except Exception as e:
        return f"An error occurred: {e}"

def save_base64_to_file(base64_string, file_path):
    """
    Save a Base64 string to a specified file.

    Parameters:
    - base64_string (str): The Base64 encoded string.
    - file_path (str): The file path where the Base64 string will be saved.

    Returns:
    - str: A message indicating success or failure.
    """
    try:
        with open(file_path, 'w') as f:
            f.write(base64_string)
        return "Base64 string saved successfully."
    except Exception as e:
        return f"An error occurred while saving: {e}"

def save_base64_to_json(base64_string, json_file_path, json_key):
    """
    Save a Base64 string to a specified key in a JSON file.

    Parameters:
    - base64_string (str): The Base64 encoded string.
    - json_file_path (str): The file path to the JSON file.
    - json_key (str): The key in the JSON file where the Base64 string will be saved.

    Returns:
    - str: A message indicating success or failure.
    """
    try:
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r') as f:
                json_data = json.load(f)
        else:
            json_data = {}
        
        json_data[json_key] = base64_string
        with open(json_file_path, 'w') as f:
            json.dump(json_data, f)
        return "Base64 string saved to JSON file successfully."
    except Exception as e:
        return f"An error occurred while saving to JSON file: {e}"

parser = argparse.ArgumentParser(description='Convert images to Base64 strings.')
parser.add_argument('default_file', type=str, nargs='?', help='The file path to a single image you want to convert. Used for default behavior.')
parser.add_argument('--files', type=str, nargs='*', help='The file paths to the images you want to convert.')
parser.add_argument('--file', type=str, help='The file path where a single Base64 string or JSON data will be saved. Optional.')
parser.add_argument('--path', type=str, help='The directory path where multiple Base64 text files will be saved. Optional.')
parser.add_argument('--key', type=str, help='The key in the JSON file where the Base64 string will be saved. Requires --file. Optional.')
args = parser.parse_args()

if args.default_file:
    base64_string = convert_file_to_base64(args.default_image)
    print("Here is your Base64 string, press Enter to continue:")
    input(base64_string)
elif args.key and not args.file:
    print("The --key argument requires --file.")
elif args.file and args.path:
    print("Please choose either --file or --path, not both.")
elif args.file:
    base64_string = convert_file_to_base64(args.files[0])
    if args.key:
        message = save_base64_to_json(base64_string, args.file, args.key)
    else:
        message = save_base64_to_json(base64_string, args.file)
    print(message)
elif args.path:
    for image in args.files:
        base64_string = convert_file_to_base64(image)
        file_name = os.path.basename(image) + '.txt'
        file_path = os.path.join(args.path, file_name)
        message = save_base64_to_file(base64_string, file_path)
        print(f"{image}: {message}")
else:
    for image in args.files:
        base64_string = convert_file_to_base64(image)
        print(f"{image}: {base64_string}")