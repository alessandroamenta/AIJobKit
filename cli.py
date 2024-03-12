import os

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

def write_to_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

def run_script(script_name):
    print(f"Running {script_name}...")
    os.system(f"python {script_name}")

def confirm_context(file_path, context_name):
    while True:
        confirmation = input(f"Have you added the {context_name} in the file '{file_path}'? (yes/no): ").strip().lower()
        if confirmation == 'yes':
            return True
        elif confirmation == 'no':
            return False
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

def empty_file(file_path):
    with open(file_path, 'w') as file:
        file.write('')

if __name__ == "__main__":
    recruiter_context_file = "./context/recruiter_context.txt"
    company_context_file = "./context/company_context.txt"
    job_description_file = "./context/jd.txt"

    # Confirm context files
    if not confirm_context(recruiter_context_file, "recruiter profile context"):
        print("Please add the recruiter profile context in the file './context/recruiter_context.txt' and run the script again.")
        exit(1)

    if not confirm_context(company_context_file, "company context"):
        print("Please add the company context in the file './context/company_context.txt' and run the script again.")
        exit(1)

    if not confirm_context(job_description_file, "job description"):
        print("Please add the job description in the file './context/jd.txt' and run the script again.")
        exit(1)

    # Run app.py
    run_script("app.py")

    # Run cold.py
    run_script("cold.py")

    print("Process completed.")

    # Empty context files
    empty_file(recruiter_context_file)
    empty_file(company_context_file)
    empty_file(job_description_file)

    print("Context files emptied.")