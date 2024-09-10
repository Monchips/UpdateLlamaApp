import requests
import json

# The API endpoint URL
url = 'https://updatellamaapp.onrender.com/send-slack-message'

# The Bearer token for authentication
headers = {
    'Authorization': 'Bearer 2a3f5bcb-4bce-47b4-81e8-a4fdd4b8e0a5',  # Replace with your actual Bearer token (e.g., User1's token)
    'Content-Type': 'application/json'  # Specify that the content is JSON
}

# The data to send in the request
payload = {
    "channel_name": "testing",  # Replace with your Slack channel
    "message": "test"
}

# Send the POST request
response = requests.post(url, headers=headers, data=json.dumps(payload))

# Check the response
if response.status_code == 200:
    print("Message sent successfully!")
    print("Response:", response.json())  # Print the full response from your API
else:
    print(f"Failed to send message. Status code: {response.status_code}")
    print("Response:", response.json())  # Print the error response
