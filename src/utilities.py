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
        messages=messages,
        top_p=top_p,
        temperature=temperature
    )
    return response.choices[0].message.content
    # return response

def call_openai_api_QA(messages, top_p=0.1, temperature=0.1, model="gpt-3.5-turbo-1106"):
    response = client.chat.completions.create(
        model=model,
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
        ret_response += response.choices[0].message.content
    return ret_response