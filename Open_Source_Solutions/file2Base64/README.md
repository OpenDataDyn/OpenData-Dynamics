# Base64 File Conversion Tool

## About

This is a Python tool for converting files to Base64 strings. It is one of the initial tools developed under OpenData Dynamics, a data conversion business that focuses on open-source solutions and community engagement.

## Features

- Convert any file to a Base64 string.
- Save the Base64 string to a file.
- Save the Base64 string to a specific key in a JSON file.

## Usage

### Convert a Single File

To convert a single file and display the Base64 string on the screen:

\`\`\`bash
python main.py your_file.txt
\`\`\`
...

### Convert a Single File

To convert a single file and save it to a file:

\`\`\`bash
python main.py your_file.txt base64_file.txt
\`\`\`
...

#### Convert and Save Multiple Text Files

To convert a multiple files and save it to files (image_name.txt) at the path:

\`\`\`bash
python main.py --files file1.txt file2.txt --path /path/to/save/
\`\`\`

#### Save to a New JSON File

To convert a single file and save it to a new json file and key:

\`\`\`bash
python main.py --files your_file.txt --file new_data.json --key new_key
\`\`\`

#### Save a PDF File to an Existing JSON File

To convert a single file and save it to a existing json file and key:

\`\`\`bash
python main.py --files your_pdf_file.pdf --file existing_data.json --key pdf_key
\`\`\`

## Tips for Using Batch/Shell Scripts

You can make the tool even more accessible by creating batch or shell scripts that act as shortcuts for different functionalities. Below are some examples:

### Windows Batch Script (main.bat)

To simply drag and drop files for conversion, create a `.bat` file with the following content:

\`\`\`batch
python main.py %*
\`\`\`

### Linux/Mac Shell Script (main.sh)

To convert a file and save it to a specific location, create a `.sh` script like this:

\`\`\`bash
#!/bin/bash
python main.py --files \$1 --file /path/to/save/output.txt
\`\`\`

Make the script executable:

\`\`\`bash
chmod +x main.sh
\`\`\`

### Complex Shell Script

To convert a file and save its Base64 string to a specific key in an existing JSON file, use:

\`\`\`bash
#!/bin/bash
python main.py --files \$1 --file existing_data.json --key your_key
\`\`\`

Remember to make the script executable as well.

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