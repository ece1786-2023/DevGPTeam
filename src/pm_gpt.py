import json
import os
import utilities
from utilities import color

from gpt_agent_config.pm_config import PM_GPT_SYSTEM_CONTEXT

def extract_req(text):
    start_marker = "<REQ_START>"
    end_marker = "<REQ_END>"
    start_index = text.find(start_marker)
    if start_index == -1:
        return "Start marker not found"

    # Adjust start_index to get the end of the start_marker
    start_index += len(start_marker)

    end_index = text.find(end_marker, start_index)
    if end_index == -1:
        return "End marker not found"

    # Extract the part of the string between the markers
    return text[start_index:end_index]


# src/pm_gpt.py
def refine_requirements(initial_requirement):
    messages = [
        {"role": "system", "content": PM_GPT_SYSTEM_CONTEXT},
        {"role": "user", "content": initial_requirement}
    ]
    # print(color.BOLD + color.GREEN + "user: " + color.END + initial_requirement)
    while True:
        response = utilities.call_openai_api_PM(messages, model="gpt-4-1106-preview")
        messages.append({"role": "assistant", "content": response})        

        # if the assistant repsonse contains the final requirement, break clarifying loop
        if "<REQ_START>" in response:
            refined_requirement = extract_req(response)
            break
        print(color.BOLD + color.YELLOW + "assistant: " + color.END, end=' ')
        utilities.print_message(response)
        
        # else, continue iteration
        user_input = input(color.BOLD + color.GREEN + "user: " + color.END)
        messages.append({"role": "user", "content": user_input})

    return refined_requirement