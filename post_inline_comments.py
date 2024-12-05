import json
import requests
import os

# Load SQLFluff report
with open('sqlfluff_report.json', 'r') as file:
    report = json.load(file)

# Extract issues
comments = []
for result in report:
    for violation in result.get('violations', []):
        line_no = violation.get('start_line_no', None)
        if line_no is not None:
            comments.append({
                "path": result["filepath"],
                "line": line_no,
                "body": f"SQLFluff violation: {violation['description']}"
            })

# Post inline comments to PR
github_token = os.getenv('GITHUB_TOKEN')
repo = os.getenv('GITHUB_REPOSITORY')
pr_number = os.getenv('PR_NUMBER')
owner = repo.split('/')[0]  # Extract the owner from the repo
source_branch = os.getenv('GITHUB_HEAD_REF')  # Source branch of the PR
target_branch = os.getenv('GITHUB_BASE_REF')  # Target branch of the PR
print(source_branch,target_branch, github_token, owner, repo)
print(f"GitHub Token: {github_token}")  # **Sensitive - Remove After Debugging**
commit_sha = source_branch

# Fetch the latest commit ID dynamically from the PR commits
commits_url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/commits"
print(commits_url)
headers = {
    "Authorization": f"Bearer {github_token}",
    "Accept": "application/vnd.github+json",
    'X-GitHub-Api-Version': '2022-11-28'
}

# Get the latest commit from the PR commits
response = requests.get(commits_url, headers=headers)
print(response)
if response.status_code == 200:
    commits = response.json()
    if commits:
        commit_id = commits[-1]['sha']  # Get the latest commit SHA
        print(f"Latest commit ID: {commit_id}")
    else:
        print("No commits found for this pull request.")
else:
    print(f"Error fetching commits: {response.status_code} - {response.text}")
    commit_id = None


# Consolidate all comments into a single comment body
if commit_id:
    consolidated_body = f"### SQLFluff Violations Report\n\n"
    consolidated_body += f"#### Based on Commit ID: `{commit_id}`\n\n"
    for comment in comments:
        consolidated_body += (
            f"- **File:** `{comment['path']}`\n"
            f"  - **Line:** {comment['line']}\n"
            f"  - **Description:** {comment['body']}\n\n"
        )

    # URL to post a general comment to the pull request
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    payload = {"body": consolidated_body}

    # Sending the POST request to GitHub API
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 201:
        print("Consolidated comment posted successfully!")
    else:
        print(f"Error posting consolidated comment: {response.status_code} - {response.text}")


# If commit_id is fetched, proceed with adding comments
# if commit_id:
#     for comment in comments:
#         url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/comments"
#         payload = {
#             "body": comment["body"],
#             "commit_id": commit_id,  # Use dynamically fetched commit_id
#             "path": comment["path"],  # Path of the file in the PR
#             "line": comment["line"],  # Line number where comment is made
#             "side": "RIGHT"  # Use LEFT or RIGHT for the diff view side
#         }

#         # Sending the POST request to GitHub API
#         response = requests.post(url, json=payload, headers=headers)

#         if response.status_code == 201:
#             print(f"Comment posted successfully: {comment['body']}")
#         else:
#             print(f"Error posting comment: {response.status_code} - {response.text}")
