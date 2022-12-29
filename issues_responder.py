import os
from time import sleep
import requests
import configparser
import openai


# Extract the secrets from the configuration data
github_token = os.environ['GITHUB_TOKEN']
openai_token = os.environ['OPENAI_SDK']


# Replace with the owner, repository name, and issue number of your repository
owner = "TheSeanLavery"
repo = "code-review-gpt"

# Set the API key for the openai library
openai.api_key = openai_token

# Fetch the details of the issue
headers = {
    "Authorization": f"Bearer {github_token}",
    "Accept": "application/vnd.github+json"
}

def generate_reply_to_issue(issue_number):
    # Fetch the details of the issue
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"
    response = requests.get(url, headers=headers)
    issue = response.json()
    # Check if the issue has any comments
    if "comments" in issue and issue["comments"] > 0:
        # Fetch the comments on the issue
        url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/comments"
        response = requests.get(url, headers=headers)
        comments = response.json()
        # Iterate through the comments
        for comment in comments:
            # Check if the comment is from the bot
            if comment["user"]["login"] == "code-review-gpt":
                # The bot has already commented on the issue
                return
    # Generate a response to the issue
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Write a code review as if you were an expert senior developer, please note where the code could be made faster, or changed to be more readable, if there is a lack of comment, or the code doesn't document it self also point it out.\n\nHere is the code to review:\n\n",
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # Format the response
    reply = f"""{response["choices"][0]["text"]}
    \n\n---\n\nI am a bot, and this action was performed automatically. Please [contact the author](Sean Lavery) if you have any questions or feedback."""
    return reply

def get_open_ai_result(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # Post the response to the issue
    data = {
        "body": response["choices"][0]["text"]
    }
    return data

def get_github_rate_limit():
    # Fetch the rate limit details
    url = "https://api.github.com/rate_limit"
    response = requests.get(url, headers=headers)
    rate_limit = response.json()
    #pretty print the rate limit
    print("Rate limit:")
    print(f"  Core limit: {rate_limit['resources']['core']['limit']}")
    print(f"  Core remaining: {rate_limit['resources']['core']['remaining']}")
    print(f"  Core reset: {rate_limit['resources']['core']['reset']}")
    print(f"  Search limit: {rate_limit['resources']['search']['limit']}")
    print(f"  Search remaining: {rate_limit['resources']['search']['remaining']}")
    print(f"  Search reset: {rate_limit['resources']['search']['reset']}")


    return rate_limit

def reply_to_issue(issue_number, comment):
    # Add a comment to the issue
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/comments"
    data = {"body": comment}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print("Comment added to issue")
    else:
        print("Error adding comment to issue")

def get_list_of_issues():
    #get list of issues
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    response = requests.get(url, headers=headers)
    issues = response.json()
    return issues

def get_latest_comment(issue_number):
    # Fetch the comments on the issue
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/comments"
    response = requests.get(url, headers=headers)
    comments = response.json()
    # Check if the latest comment is by the bot
    latest_comment = comments[-1]
    return latest_comment

def respond_to_issue(issue_number):
    # Fetch the details of the issue
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"
    response = requests.get(url, headers=headers)
    issue = response.json()
   
    # Check if the issue has any comments
    if "comments" in issue and issue["comments"] > 0:
        latest_comment = get_latest_comment(issue_number)
        if latest_comment["user"]["login"] != "CodeReviewGPT":
            # Generate a response to the latest comment using OpenAI
            body = latest_comment["body"]
            data = get_open_ai_result("write a response to this comment:\n\n" + body + "\n\n")
            
            url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue['number']}/comments"
            response = requests.post(url, headers=headers, json=data)
            print(response.json())
        else:
            print("The latest comment was by the bot")
    else:
        print("The issue has no comments")
        # Generate a response to the issue using OpenAI
        body = issue["body"]
        data = get_open_ai_result("write a response to this issue:\n\n" + body + "\n\n")
        url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue['number']}/comments"
        response = requests.post(url, headers=headers, json=data)
   
def ReplyToAllIssues():
    issues = get_list_of_issues()
    # Reply with OpenAI to issues that have been commented on by other users
    for issue in issues:
        respond_to_issue(issue["number"])

get_github_rate_limit()

