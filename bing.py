import requests

# Define the API endpoint
url = "https://bing.com/chat/api"

# Define the API parameters
params = {
    "user_id": "YOUR_USER_ID", # Replace with your user ID
    "chat_id": "YOUR_CHAT_ID", # Replace with your chat ID
    "mode": "Balanced" # Replace with your chat mode
}

# Make the API request
response = requests.get(url, params=params)
data = response.json()

# Extract the chat history
chat_history = data["chat_history"]

# Define the file name and location
file_name = "chat_history.txt"
file_location = "YOUR_FILE_LOCATION" # Replace with your file location

# Save the chat history to a file
with open(file_location + file_name, "w") as file:
    for message in chat_history:
        file.write(message + "\n")
