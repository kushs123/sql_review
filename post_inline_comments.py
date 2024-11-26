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
         line_no = violation.get('start_line_no', None)  # Default to None if the key is missing
        if line_no is not None:  # Ensure that the line number exists
            comments.append({
                "path": result["filepath"],
                "line": line_no,
                "body": f"SQLFluff violation: {violation['description']}"
            })
# Post inline comments to PR
github_token = os.getenv('GITHUB_TOKEN')
repo = os.getenv('GITHUB_REPOSITORY')
pr_number = os.getenv('PR_NUMBER')

for comment in comments:
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/comments"
    payload = {
        "path": comment["path"],
        "line": comment["line"],
        "body": comment["body"]
    }
    headers = {"Authorization": f"Bearer {github_token}"}
    requests.post(url, json=payload, headers=headers)
