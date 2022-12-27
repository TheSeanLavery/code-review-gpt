import webbrowser

# Provide some help to the user
print("\nYou can obtain your GitHub token at the following URL: https://github.com/settings/tokens")
print("You can obtain your OpenAI SDK key at the following URL: https://beta.openai.com/account/api-keys")
#newline
print(" ")

# Prompt the user for their GitHub and OpenAI SDK keys
github_token = input("Enter your GitHub token: ")
openai_sdk = input("Enter your OpenAI SDK key: ")

# Create the contents of the secrets.conf file
contents = "[DEFAULT]\nGITHUB_TOKEN={}\nOPENAI_SDK={}".format(github_token, openai_sdk)

# Write the contents to the secrets.conf file
with open("secrets.conf", "w") as f:
    f.write(contents)

print("\nYour secrets.conf file has been created with the following contents:\n")
print(contents)
