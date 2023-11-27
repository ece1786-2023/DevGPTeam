import sys
import argparse
import json

import pm_gpt
import dev_gpt
import qa_gpt
import utilities
from utilities import color

def main():
    refined_requirement = None
    generated_code = None
    snapshot_project_name = None

    parser = argparse.ArgumentParser(description="Usage:")

    # Add arguments
    parser.add_argument("--skipPM", action="store_true", help="Disable PM GPT (Code Review)")
    parser.add_argument("--skipDev", action="store_true", help="Disable Dev GPT (Code Review)")
    parser.add_argument("--skipQA", action="store_true", help="Disable QA GPT (Code Review)")
    parser.add_argument("--snapshot-directory", type=str, help="Regenerate source code base on checkpoint file (.json)")

    # Parse arguments
    args = parser.parse_args()

    if args.snapshot_directory is not None:
        snapshot_project_name = args.snapshot_directory
        print(f"snapshot path is set to: {snapshot_project_name}")

        with open('workspace/{}/{}.json'.format(snapshot_project_name, snapshot_project_name), 'r') as file:
            project = json.load(file)

            refined_requirement, generated_code = project["refine_requirements"], project["developed_code"]

    print(color.BOLD + color.PURPLE + "Welcome to Dev GPTeam!" + color.END)

    # PM GPT clarifying requirements
    if refined_requirement and (args.skipPM or args.skipDev):
        print("Found project requirement from checkpoint file")
    else:
        print(color.BOLD + color.YELLOW + "assistant: " + color.END + "Please enter your initial requirement: " )
        initial_requirement = input(color.BOLD + color.GREEN + "user: " + color.END)
        refined_requirement = pm_gpt.refine_requirements(initial_requirement)

    print(color.BOLD + color.BLUE + "Finalized Requirements:\n" + color.END, end='')
    utilities.print_message(refined_requirement)

    # Dev GPT generating code
    if generated_code and (args.skipDev):
        print("Found generated from checkpoint file")
    else:        
        print(color.BOLD + color.PURPLE + "Generating code...\n" + color.END)
        generated_code = dev_gpt.generate_code(refined_requirement)

    print(color.BOLD + color.BLUE + "Generated code:\n" + color.END, end='')
    utilities.print_message(generated_code)

    finalized_code = None 

    if args.skipQA:
        print("Not Using QA")

        # only Dev Write to dir
        utilities.parse_code(generated_code, "", snapshot_project_name)   
        utilities.take_project_info_snapshot(refined_requirement, generated_code, None, snapshot_project_name)

    else:
        # Dev Write to dir
        utilities.parse_code(generated_code, "-dev", snapshot_project_name)
        utilities.take_project_info_snapshot(refined_requirement, generated_code, finalized_code, snapshot_project_name)

        # QA GPT review code
        print(color.BOLD + color.PURPLE + "Reviewing code...\n" + color.END)
        finalized_code = qa_gpt.code_review(refined_requirement, generated_code)
        print(color.BOLD + color.BLUE + "Code review feedback:\n" + color.END, end='')
        utilities.print_message(finalized_code)

        # QA Write to dir
        utilities.parse_code(finalized_code, "", snapshot_project_name)
        utilities.take_project_info_snapshot(refined_requirement, generated_code, finalized_code, snapshot_project_name)

    print(color.BOLD + color.PURPLE + "Completed!!! Run the code in the workspace." + color.END)

if __name__ == "__main__":
    main()
