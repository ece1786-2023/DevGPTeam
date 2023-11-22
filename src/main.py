import sys
import argparse
import json

import pm_gpt
import dev_gpt
import qa_gpt
import utilities
from utilities import color

def main():
    skip_dev = False
    skip_pm = False
    use_qa = True

    parser = argparse.ArgumentParser(description="Usage:")

    # Add arguments
    parser.add_argument("--skipPM", action="store_true", help="Disable PM GPT (Code Review)")
    parser.add_argument("--skipDev", action="store_true", help="Disable Dev GPT (Code Review)")
    parser.add_argument("--noQA", action="store_true", help="Disable QA GPT (Code Review)")
    parser.add_argument("--snapshot-directory", type=str, help="Regenerate source code base on checkpoint file (.json)")

    # Parse arguments
    args = parser.parse_args()

    if args.noQA:
        use_qa = False
        print("Not Using QA")

    if args.snapshot_directory is not None:
        print(f"snapshot path is set to: {args.snapshot_directory}")

        with open('workspace/{}/{}.json'.format(args.snapshot_directory, args.snapshot_directory), 'r') as file:
            project = json.load(file)

    refined_requirement, generated_code = project["refine_requirements"], project["developed_code"]

    print(color.BOLD + color.PURPLE + "Welcome to Dev GPTeam!" + color.END)

    # PM GPT clarifying requirements
    if refined_requirement and (args.skipPM or args.skipDev):
        print("Found project requirement from checkpoint file")
    else:
        initial_requirement = input(color.BOLD + color.YELLOW + "Assistant: " + color.END + "Please enter your initial requirement: " )
        refined_requirement = pm_gpt.refine_requirements(initial_requirement)

    print(color.BOLD + color.BLUE + "Finalized Requirements:\n" + color.END + refined_requirement)

    # Dev GPT generating code
    if generated_code and (args.skipDev):
        print("Found generated from checkpoint file")
    else:        
        print(color.BOLD + color.PURPLE + "Generating code...\n" + color.END)
        generated_code = dev_gpt.generate_code(refined_requirement)

    print(color.BOLD + color.BLUE + "Generated code:\n" + color.END + generated_code)

    finalized_code = None 
    if use_qa:
        # QA GPT review code
        print(color.BOLD + color.PURPLE + "Reviewing code...\n" + color.END)
        finalized_code = qa_gpt.code_review(refined_requirement, generated_code)
        print(color.BOLD + color.BLUE + "Code review feedback:\n" + color.END + finalized_code)

    utilities.parse_code(generated_code)
    utilities.take_project_info_snapshot(refined_requirement, generated_code, finalized_code)

    print(color.BOLD + color.PURPLE + "Completed!!! Run the code in the workspace." + color.END)

if __name__ == "__main__":
    main()
