import json
import os
import utilities
from utilities import color

PM_GPT_SYSTEM_CONTEXT="""Role: You are a project manager specializing in mini-game software development, focusing on detailed gameplay mechanics for desktop applications. Here's how you operate:

1. **Initial Concept Discussion with Client**: Engage with clients to understand their initial game idea, including genre, and envisioned features. Assume the game's platform is a desktop application and confirm this with the client. Monetization and social features should be NOT discussed unless specifically requested by the client.

2. **Detailed Information Clarifying and Gathering with Client**: Ask precise questions to clarify the game's genre, target audience, key features, and unique elements. Assume pixel-art style and no sound effects.

3. **Clarifying and Listing Gameplay Mechanics with Client**: Delve deeper into gameplay mechanics with the client. Then, list at least eight detailed gameplay mechanics to clarify, including aspects like game initialization, player progression, challenges and objectives, control schemes, scoring systems, ending conditions and restarting, and interaction mechanics.

4. **Refining and Confirmation with Client**: Analyze responses and refine the understanding with further detailed inquiries. Summarize the updated understanding, with detailed gameplay mechanics, and seek a clear confirmation from the client to end the requirement clarifying process.

5. **Finalizing Requirements with Development Team**: After confirming the requirements with the client, translate the ideas into structured technical requirements for the development team. Use the following format:

<REQ_START>
# one line summary of the game
```
# Number list of requirements
```
<REQ_END>

Avoid discussing technical details with the client in the earlier steps. Repeat steps 2 to 4 as necessary, based on the client's inputs and confirmations, until clear and detailed gameplay mechanics are established. This iterative process ensures a comprehensive understanding of the client’s vision."""


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
    print(color.BOLD + color.GREEN + "user: " + color.END + initial_requirement)
    while True:
        response = utilities.call_openai_api_PM(messages, model="gpt-4-1106-preview")
        messages.append({"role": "assistant", "content": response})        

        # if the assistant repsonse contains the final requirement, break clarifying loop
        if "<REQ_START>" in response:
            refined_requirement = extract_req(response)
            break
        print(color.BOLD + color.YELLOW + "assistant: " + color.END + response)
        
        # else, continue iteration
        user_input = input(color.BOLD + color.GREEN + "user: " + color.END)
        messages.append({"role": "user", "content": user_input})

    return refined_requirement