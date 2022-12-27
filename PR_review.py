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

    # Iterate through each pull request
    for pull_request in pull_requests:
        # Get the number of the pull request
        number = pull_request["number"]

        # Initialize the list of changes
        changes = []

        # Get the list of changes for the pull request
        response = requests.get(f"{base_url}/repos/{owner}/{repo}/pulls/{number}/files", headers=headers)

        # Check the status code to make sure the request was successful
        if response.status_code == 200:
            # Get the list of changes
            changes = response.json()
            
            newChanges = ''
            # Iterate through each change and add the number of lines added and removed to the list
            for change in changes:
                #add the lines of code that were changed
                newChanges+=(f"{change['patch']}")
                newChanges+=("\n")
        else:
            print(f"Error getting changes for pull request {number}: {response.status_code} {response.reason}")

        # Get the title and body of the pull request
        title = pull_request["title"]
        body = pull_request["body"]

        # Combine the title, body, and list of changes into a single string 
        text = " Review this code as if you were a Lead Dev. Decide if its good or what should be changed, be very thourough, call out lines of code and format them in a markdown block and explain what should be changed: \n" + title+ "\n" +body+ "\n" +(newChanges)

        print(text)

        response = openai.Completion.create(
                  model="text-davinci-003",
                  prompt=text,
                  temperature=0.7,
                  max_tokens=256,
                  top_p=1,
                  frequency_penalty=0,
                  presence_penalty=0
                )

        # Get the generated response
        openai_response = response["choices"][0]["text"]

        # Post the generated response as a comment on the pull request
        response = requests.post(
            f"{base_url}/repos/{owner}/{repo}/issues/{number}/comments",
            headers=headers,
            json={"body": openai_response}
        )

        # Check the status code to make sure the request was successful
        if response.status_code == 201:
            print(f"Comment posted successfully on pull request {number}")
        else:
            print(f"Error posting comment on pull request {number}: {response.status_code} {response.reason}")
else:
    print(f"Error getting pull requests: {response.status_code} {response.reason}")