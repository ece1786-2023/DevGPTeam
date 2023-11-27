import http.client
import json
import os

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY') 
OPENAI_API_ENDPOINT = os.getenv('OPENAI_API_ENDPOINT') 

def call_openai_api_DEV(system_context, user_prompt, top_p, temperature=1, model="gpt-3.5-turbo-1106"):
    response = client.chat.completions.create(
        model=model,
        #model="gpt-4-1106-preview",
        #model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "system", "content": system_context},
            {"role": "user", "content": user_prompt}
        ],
        top_p=top_p,
        temperature=temperature
    )
    #return response.choices[0].message.content
    return response

def call_openai_api_PM(messages, top_p=0.5, temperature=0.7, model="gpt-3.5-turbo-1106"):
    response = client.chat.completions.create(
        model=model,
        #model="gpt-3.5-turbo-1106",
        messages=messages,
        top_p=top_p,
        temperature=temperature
    )
    return response.choices[0].message.content
    # return response

def call_openai_api_QA(messages, top_p=0.1, temperature=0.1, model="gpt-3.5-turbo-1106"):
    response = client.chat.completions.create(
        model=model,
        #model="gpt-3.5-turbo-1106",
        messages=messages,
        top_p=top_p,
        temperature=temperature
    )
    ret_response = response.choices[0].message.content
    while response.choices[0].finish_reason != "stop":
        msg = messages.append({"role":"assistant", "content":response})
        response = client.chat.completions.create(
            model=model,
            messages=msg,
            top_p=top_p,
            temperature=temperature
        )
        print("keep generating!")
        ret_response += response.choices[0].message.content
    return ret_response

def get_project_name(code_string):
    # Extract project name between the new tags
    project_start_tag = "<PROJECT_NAME_START>"
    project_end_tag = "<PROJECT_NAME_END>"
    project_name_start = code_string.find(project_start_tag) + len(project_start_tag)
    project_name_end = code_string.find(project_end_tag)
    project_name = code_string[project_name_start:project_name_end].strip()
    
    return project_name

def parse_code(code_string, project_name_suffix, project_name=None):
    # Get the directory of the main.py file
    main_file_dir = os.path.dirname(os.path.abspath(__file__))

    if not project_name:
        project_name = get_project_name(code_string)

    project_name = project_name + project_name_suffix

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

        # Check if the section contains Python code
        if "```python" in file_content:
            # Split each file content into filename and code
            filename_and_code = file_content.split("```python\n", 1)
            filename = filename_and_code[0].strip()
            code = filename_and_code[1].strip("```\n").strip()

            # Write the code to a file in the project workspace directory
            file_path = os.path.join(project_workspace_path, filename)
            with open(file_path, 'w') as file:
                file.write(code)


def take_project_info_snapshot(refine_requirements, developed_code, finalized_code, project_name=None):
    # Get the directory of the main.py file
    main_file_dir = os.path.dirname(os.path.abspath(__file__))

    if not project_name:
        project_name = get_project_name(developed_code)

    # Define the workspace path relative to the main.py file
    project_workspace_path = os.path.join(main_file_dir, f'../workspace/{project_name}')

    # Ensure the project workspace directory exists
    os.makedirs(project_workspace_path, exist_ok=True)

    data = {
        'refine_requirements': refine_requirements,
        'developed_code': developed_code,
        'finalized_code': finalized_code
    }

    file_path = os.path.join(project_workspace_path, project_name + ".json")

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'