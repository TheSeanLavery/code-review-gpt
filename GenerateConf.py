import os
import webbrowser
import requests
import openai

# Provide some help to the user
print("\nYou can obtain your GitHub token at the following URL: https://github.com/settings/tokens")
print("You can obtain your OpenAI SDK key at the following URL: https://beta.openai.com/account/api-keys")
#newline
print(" ")

#if if the config file already exists, ask the user if they want to overwrite it
if os.path.exists("secrets.conf"):
    overwrite = input("A secrets.conf file already exists. Do you want to overwrite it? (y/n): ")
    if overwrite.lower() == "n":
        print("Exiting the program...")
        exit()

# Prompt the user for their GitHub and OpenAI SDK keys
github_token = input("Enter your GitHub token: ")
openai_sdk = input("Enter your OpenAI SDK key: ")

# Validate the GitHub token
api_endpoint = "https://api.github.com/user"
headers = {"Authorization": f"Bearer {github_token}"}
response = requests.get(api_endpoint, headers=headers)
if response.status_code == 200:
    print("GitHub token is valid")
else:
    print("GitHub token is invalid")

# Validate the OpenAI SDK key
openai.api_key = openai_sdk
try:
    models = openai.Model.list()
    print("OpenAI SDK key is valid")
except openai.api_errors.ApiError as err:
    print("OpenAI SDK key is invalid")


# Create the contents of the secrets.conf file
contents = "[DEFAULT]\nGITHUB_TOKEN={}\nOPENAI_SDK={}".format(github_token, openai_sdk)

# Write the contents to the secrets.conf file
with open("secrets.conf", "w") as f:
    f.write(contents)

print("\nYour secrets.conf file has been created with the following contents:\n")
print(contents)
