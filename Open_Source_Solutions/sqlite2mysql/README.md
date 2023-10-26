
# CSV to JSON Conversion Tool


## About

This is a Python tool for converting CSV files to JSON format. It is one of the initial tools developed under OpenData Dynamics, a data conversion business that focuses on open-source solutions and community engagement.

## Features

- Convert one or multiple CSV files to a JSON file.
- Support for custom CSV delimiters.
- Support for different file encodings.
- Optional column filtering.
- Nest CSV data under a specific key in the JSON.

## Usage

### Convert a Single CSV File

To convert a single CSV file and save the JSON data to a file:

```bash
python main.py --csv_files your_file.csv --json_file output.json
```

### Convert Multiple CSV Files

To convert multiple CSV files and save them to a single JSON file:

```bash
python main.py --csv_files file1.csv file2.csv --json_file output.json
```

### Custom Delimiter

To specify a custom delimiter in the CSV files:

```bash
python main.py --csv_files your_file.csv --json_file output.json --delimiter ';'
```

### Specify Columns

To only include specific columns in the JSON output:

```bash
python main.py --csv_files your_file.csv --json_file output.json --columns name age
```

### Save to a Nested Key in JSON

To save the CSV data under a specific key in the JSON file:

```bash
python main.py --csv_files your_file.csv --json_file existing.json --key data_key
```

## Tips for Using Batch/Shell Scripts

You can make the tool even more accessible by creating batch or shell scripts that act as shortcuts for different functionalities. Below are some examples:

### Windows Batch Script (main.bat)

To simply drag and drop files for conversion, create a `.bat` file with the following content:

```batch
python main.py %*
```

### Linux/Mac Shell Script (main.sh)

To convert a file and save it to a specific location, create a `.sh` script like this:

```bash
#!/bin/bash
python main.py --csv_files $1 --json_file /path/to/save/output.json
```

Make the script executable:

```bash
chmod +x main.sh
```

These are just a few examples. Feel free to tailor the scripts according to your specific needs.

## License

Copyright 2023 OpenData Dynamics

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

## Contacts

[Link to OpenData Dynamics EMail](mailto:opendatadynamics@gmail.com)

[Link to OpenData Dynamics X/Twitter](https://twitter.com/OpenDataDyn)

[Link to OpenData Dynamics Reddit](https://www.reddit.com/user/OpenDataDynamics)

[Link to OpenData Dynamics GitHub Repository](https://github.com/TheCompAce/OpenData-Dynamics)