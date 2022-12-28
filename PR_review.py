import logging
import requests
import configparser
import openai

# Read the secrets from the configuration file
config = configparser.ConfigParser()
config.read("secrets.conf")

# Extract the secrets from the configuration data
github_token = config["DEFAULT"]["GITHUB_TOKEN"]
openai_sdk_token = config["DEFAULT"]["OPENAI_SDK"]

# Replace with the owner, repository name, and issue number of your repository
owner = "TheSeanLavery"
repo = "code-review-gpt"
issue_number = 1

# Set the API key for the openai library
openai.api_key = openai_sdk_token

# Set the base URL for the GitHub API
base_url = "https://api.github.com"

# Set the headers for the HTTP requests
headers = {
    "Authorization": f"Token {github_token}",
    "Accept": "application/vnd.github+json",
    "Content-Type": "application/json"
}

# Get the list of pull requests for the repository
response = requests.get(f"{base_url}/repos/{owner}/{repo}/pulls", headers=headers)

# Check the status code to make sure the request was successful
if response.status_code == 200:
    # Get the list of pull requests
    pull_requests = response.json()

    # Initialize the list of changes
    new_changes = ''

    # Initialize the text variable
    text = ''

    # Initialize the openai_response variable
    openai_response = ''

    # Iterate through each pull request
    for pull_request in pull_requests:

        pull_request = requests.get(f"{base_url}/repos/{owner}/{repo}/pulls/{number}", headers=headers)

        if pull_request.status_code == 200:
            pull_request = pull_request.json()
        else:
            logging.error(f"Error getting pull request {number}: {pull_request.status_code} {pull_request.reason}")

        # Get the number of the pull request
        number = pull_request["number"]

        # Get the list of changes for the pull request
        response = requests.get(f"{base_url}/repos/{owner}/{repo}/pulls/{number}/files", headers=headers)

        


        # Check the status code to make sure the request was successful
        if response.status_code == 200:
            # Get the list of changes
            changes = response.json()
            
            # Reset the new_changes variable for each iteration
            new_changes = ''

            # Iterate through each change and add the number of lines added and removed to the list
            for change in changes:
                #add the lines of code that were changed
                new_changes+=(f"{change['patch']}")
                new_changes+=("\n")
        else:
            logging.error(f"Error getting changes for pull request {number}: {response.status_code} {response.reason}")

        

        # Get the title and body of the pull request
        title = pull_request["title"]
        body = pull_request["body"]

        # Reset the text variable for each iteration
        text = " Review this code as if you were a Lead Dev. Give it a total score out of 100. Decide if its good or what should be changed, be very thourough, call out lines of code and format them in a markdown block and explain what should be changed: \n" + title+ "\n" +body+ "\n" +(new_changes)

        # Generate a response using the openai library
        response = openai.Completion.create(
                  model="text-davinci-003",
                  prompt=text,
                  temperature=0.7,
                  max_tokens=1000,
                  top_p=1,
                  frequency_penalty=0,
                  presence_penalty=0
                )

        # Reset the openai_response variable for each iteration
        openai_response = response["choices"][0]["text"]

        # Post the generated response as a comment on the pull request
        response = requests.post(
            f"{base_url}/repos/{owner}/{repo}/issues/{number}/comments",
            json={"body": openai_response},
            headers=headers
        )

        # Check the status code to make sure the request was successful
        if response.status_code == 201:
            logging.info(f"Successfully posted comment on pull request {number}")
        else:
            logging.error(f"Error posting comment on pull request {number}: {response.status_code} {response.reason}")
else:
    logging.error(f"Error getting pull requests: {response.status_code} {response.reason}")

    import pytest
from unittest.mock import patch

def test_requests_import():
    assert "requests" in globals()

def test_secrets_parsed():
    assert github_token == config["DEFAULT"]["GITHUB_TOKEN"]
    assert openai_sdk_token == config["DEFAULT"]["OPENAI_SDK"]

def test_headers_and_base_url_initialized():
    assert base_url == "https://api.github.com"
    assert headers["Authorization"] == f"Token {github_token}"
    assert headers["Accept"] == "application/vnd.github+json"
    assert headers["Content-Type"] == "application/json"

def test_get_pull_requests_successful():
    assert response.status_code == 200

def test_get_changes_successful():
    assert response.status_code == 200

def test_openai_call_correct():
    with patch("openai.Completion.create") as mock_create:
        openai.Completion.create(model="text-davinci-003", prompt=text, temperature=0.7, max_tokens=1000, top_p=1, frequency_penalty=0, presence_penalty=0)
        mock_create.assert_called_with(model="text-davinci-003", prompt=text, temperature=0.7, max_tokens=1000, top_p=1, frequency_penalty=0, presence_penalty=0)
