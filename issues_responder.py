import requests
import configparser
import openai

# Read the secrets from the configuration file
config = configparser.ConfigParser()
config.read("secrets.conf")

# Extract the secrets from the configuration data
github_token = config["DEFAULT"]["GITHUB_TOKEN"]
openai_token = config["DEFAULT"]["OPENAI_SDK"]

# Replace with the owner, repository name, and issue number of your repository
owner = "TheSeanLavery"
repo = "code-review-gpt"
issue_number = 1

# Set the API key for the openai library
openai.api_key = openai_token

# Fetch the details of the issue
headers = {
    "Authorization": f"Bearer {github_token}",
    "Accept": "application/vnd.github+json"
}

#get list of issues
url = f"https://api.github.com/repos/{owner}/{repo}/issues"
response = requests.get(url, headers=headers)
issues = response.json()

# Reply with OpenAI to issues that have been commented on by other users
for issue in issues:
    # Check if the issue has been created by the bot CodeReviewGPT
    if issue["user"]["login"] != "CodeReviewGPT":
        # Check if the issue has any comments
        if "comments" in issue and issue["comments"] > 0:
            # Fetch the comments on the issue
            url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue['number']}/comments"
            response = requests.get(url, headers=headers)
            comments = response.json()
            # Check if the latest comment is by the bot
            latest_comment = comments[-1]
            if latest_comment["user"]["login"] != "CodeReviewGPT":
                # Generate a response to the latest comment using OpenAI
                body = latest_comment["body"]
                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt="write a response to this comment:\n\n" + body + "\n\n",
                    temperature=0.7,
                    max_tokens=256,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                )
                # Create a comment on the issue with the generated response
                url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue['number']}/comments"
                data = {
                    "body": response["choices"][0]["text"]
                }   
                response = requests.post(url, headers=headers, json=data)
                print(response.status_code)
                print(response.json())
        # If the issue has no comments, generate a response to the issue body
        else:
            # Generate a response to the issue body using OpenAI
            body = issue["body"]
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt="Write a response to this comment as if you are a Senior Developer, be thorough, and ask questsions if the user is unclear:\n\n" + body + "\n\n",
                # Adjust the parameters to influence the quality of the response
                temperature=0.7,        # Higher values increase the creativity of the response
                max_tokens=256,         # Maximum number of tokens in the response
                top_p=1,                # The proportion of the tokens
            )
            # Create a comment on the issue with the generated response
            url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue['number']}/comments"
            data = {
                "body": response["choices"][0]["text"]
            }   
            response = requests.post(url, headers=headers, json=data)
            print(response.status_code)
            print(response.json())

