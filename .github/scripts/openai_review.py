import os
import sys
from openai import OpenAI
from github import Github

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# This function can be placed outside the main check because it does not
# depend on command line arguments or environment variables specific to the event trigger.
def get_code_review(code_snippet):
    try:
        response = client.chat.completions.create(
            model="gpt-4",  # Or whichever model you're using; "gpt-3.5-turbo" might be appropriate
            messages=[
                {"role": "system", "content": "You are an experienced software developer reviewing a piece of Python code."},
                {"role": "user", "content": f"Please review the following Python code:\n\n{code_snippet}"},
            ]
        )
        review = response.choices[0].message.content
        return review
    except Exception as e:  # Catch a general exception
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    g = Github(os.getenv('GITHUB_TOKEN'))
    repo_name = os.getenv('GITHUB_REPOSITORY')

    pr_number = None
    if 'INPUT_PR_NUMBER' in os.environ:  # Check if PR number is set in the environment
        pr_number = int(os.environ['INPUT_PR_NUMBER'])
    else:
        print("Pull Request number not found.")
        sys.exit(1)

    repo = g.get_repo(repo_name)
    pull_request = repo.get_pull(pr_number)
    files = pull_request.get_files()

    for file in files:
        if file.filename.endswith('.py'):  # Review only Python files
            print(f"Reviewing {file.filename}...")
            # You may want to retrieve the full file content here
            content_file = repo.get_contents(file.filename, ref=pull_request.head.ref)
            code_content = content_file.decoded_content.decode('utf-8')  # Get raw content of the file

            review = get_code_review(code_content)
            if review:
                print("OpenAI Code Review:")
                print(review)
                # Post the review back to the PR as a comment
                pull_request.create_issue_comment(review)
