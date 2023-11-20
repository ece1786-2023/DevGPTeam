import pm_gpt
import dev_gpt
import qa_gpt
import utilities
from utilities import color
import sys

def main():
    use_qa = True
    if len(sys.argv) > 1:
        if sys.argv[1] == "--noQA":
            use_qa = False
            print("Not Using QA")
        else:
            print("Unknown argument")
    
    print("Welcome to Dev GPTeam!")
    initial_requirement = input(color.BOLD + color.YELLOW + "Assistant: " + color.END + "Please enter your initial requirement: " )
    # PM GPT clarifying requirements
    refined_requirement = pm_gpt.refine_requirements(initial_requirement)
    print(color.BOLD + color.BLUE + "Finalized Requirements:\n" + color.END + refined_requirement)
    # Dev GPT generating code
    print(color.BOLD + color.PURPLE + "Generating code...\n" + color.END)
    generated_code = dev_gpt.generate_code(refined_requirement)
    print(color.BOLD + color.BLUE + "Generated code:\n" + color.END + generated_code)

    if use_qa:
        # QA GPT review code
        print(color.BOLD + color.PURPLE + "Reviewing code...\n" + color.END)
        finalized_code = qa_gpt.code_review(refined_requirement, generated_code)
        print(color.BOLD + color.BLUE + "Code review feedback:\n" + color.END + finalized_code)
    # write final code to workspace
    utilities.parse_code(finalized_code)
    print("Completed!!! Run the code in the workspace.")

if __name__ == "__main__":
    main()
