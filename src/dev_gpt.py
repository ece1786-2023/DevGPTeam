import json
import os
import utilities

from openai import OpenAI

client = OpenAI()
#from config.gpt_agents_config import DEV_GPT_SYSTEM_CONTEXT

DEV_GPT_SYSTEM_CONTEXT_V3="""NOTICE
Role: You are a professional software engineer; the main goal is to write PEP8 compliant, elegant, modular, easy to read and maintain Python 3.9 code. Output format strictly follow "Format example".

Write code with triple quoto, based on the following list and context.

1. You may output more than one file, but please use '<FILE_START>' and '<FILE_END>' tags to separate them.
2. Your code must be able to be run end-to-end
3. IMPORTANT: Put your generated project folder name between '<PROJECT_NAME_START>' and '<PROJECT_NAME_END>' tags.
4. Replace 'GENERATED_FILE_NAME' with the file name you propose.
5. Please assume the user will run the program by running main.py, so put the main class inside main.py.
6. Please assume all the graphic will be in pixel, avoid using extra assets like .png, .wav files.
7. The total number of lines of code generated should be less than 500.
8. Attention1: ALWAYS SET A DEFAULT VALUE, ALWAYS USE EXPLICIT VARIABLE.
9. IMPORTANT: Please implement complete code snippets.

Format Example:
-----
<PROJECT_NAME_START><PROJECT_NAME_END>
<FILE_START>
GENERATED_FILE_NAME
```python
# your code here
```
<FILE_END>
<FILE_START>
GENERATED_FILE_NAME
```python
# your code here
```
<FILE_END>
-----"""

additional_requirement="""
Additional requirement:
1. IMPORTANT: Put your generated project folder name between '<PROJECT_NAME_START>' and '<PROJECT_NAME_END>' tags.
2. Output format strictly follow "Format example" in your context or instruction.
3. Please assume all the graphic will be in pixel, avoid using extra assets like .png, .wav files.
"""


import os

def parse_code(code_string):
    # Get the directory of the main.py file
    main_file_dir = os.path.dirname(os.path.abspath(__file__))

    # Extract project name between the new tags
    project_start_tag = "<PROJECT_NAME_START>"
    project_end_tag = "<PROJECT_NAME_END>"
    project_name_start = code_string.find(project_start_tag) + len(project_start_tag)
    project_name_end = code_string.find(project_end_tag)
    project_name = code_string[project_name_start:project_name_end].strip()

    # Define the workspace path relative to the main.py file
    project_workspace_path = os.path.join(main_file_dir, f'../workspace/{project_name}')

    # Ensure the project workspace directory exists
    os.makedirs(project_workspace_path, exist_ok=True)

    # Split the string by the file start delimiter
    file_sections = code_string.split("<FILE_START>")

    for file_section in file_sections[1:]:  # Skip the first split as it's before the first FILE_START
        # Further split by the file end delimiter
        parts = file_section.split("<FILE_END>")
        file_content = parts[0].strip()  # The file content (filename + code)

        # Split each file content into filename and code
        filename_and_code = file_content.split("```python\n", 1)
        filename = filename_and_code[0].strip()
        code = filename_and_code[1].strip("```\n").strip()

        # Write the code to a file in the project workspace directory
        file_path = os.path.join(project_workspace_path, filename)
        with open(file_path, 'w') as file:
            file.write(code)

# src/dev_gpt.py
def generate_code(refined_requirement):
    with open('config/gpt_agents_config.json', 'r') as config_file:
        config = json.load(config_file)
        
    dev_gpt_config = config['DEV_GPT_CONFIG']

    print(refined_requirement + "\n" + additional_requirement)

    response = utilities.call_openai_api_DEV(DEV_GPT_SYSTEM_CONTEXT_V3, refined_requirement + "\n" + additional_requirement, 0.3, 0.3, model="gpt-4-1106-preview")
    code_string = response.choices[0].message.content
    
    print(response.choices[0].message.content)
    parse_code(code_string)

    return code_string