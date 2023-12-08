import os

import utilities
from gpt_agent_config.qa_config import QA_GPT_SYSTEM_CONTEXT

QA_GPT_TEMPERATURE_N_TOPP = float(os.getenv('QA_GPT_TEMPERATURE_N_TOPP'))

def code_review(requirement, generated_code):
    # attention: the '#' in the beginning may make GPT ignore the rest of the content 
    requirement = requirement.strip().strip("#")

    req_and_code = "Requirement:\n" + requirement + "Code to review:\n" + generated_code
    messages = [
        {"role": "system", "content": QA_GPT_SYSTEM_CONTEXT},
        {"role": "user", "content": req_and_code}
    ]
    response = utilities.call_openai_api_QA(messages, QA_GPT_TEMPERATURE_N_TOPP, QA_GPT_TEMPERATURE_N_TOPP, model="gpt-4-1106-preview")
    return response

