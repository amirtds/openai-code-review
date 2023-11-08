import os
import openai
from github import Github

# Initialize Github client with the provided GITHUB_TOKEN
g = Github(os.getenv('GITHUB_TOKEN'))

# Get the repository and pull request number from the GitHub Event context
repo_name = os.getenv('GITHUB_REPOSITORY')
pr_number = os.getenv('INPUT_PR_NUMBER')

# Retrieve the pull request
repo = g.get_repo(repo_name)
pull_request = repo.get_pull(pr_number)

# Assuming we're only interested in the changes of the last commit in the PR
files = pull_request.get_files()

# Prepare the OpenAI API call
openai.api_key = os.getenv('OPENAI_API_KEY')

def get_code_review(code_snippet):
    try:
        response = openai.Completion.create(
            engine="code-davinci-002",
            prompt=f"As an experienced developer, please review the following code:\n\n{code_snippet}\n\n"
                   "Identify any bugs, issues, security vulnerability, areas that could be improved for better performance, "
                   "readability, or maintainability. Provide your feedback in a friendly "
                   "and constructive manner, and offer a simple, step-by-step guide for "
                   "the user to make these improvements.",
            temperature=0.5,
            max_tokens=512,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=["\n\n"]
        )
        review = response.choices[0].text.strip()
        return review
    except openai.Error as e:
        print(f"An error occurred: {e}")
        return None

# Loop through the files in the PR
for file in files:
    if file.filename.endswith('.py'):  # Assuming you only want to review Python files
        print(f"Reviewing {file.filename}...")
        code_content = file.patch  # .patch will give you the diff of the file
        review = get_code_review(code_content)
        if review:
            print("OpenAI Code Review:")
            print(review)
            # Here you could post this review back to the PR as a comment
