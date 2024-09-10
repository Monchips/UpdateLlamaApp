import requests
import json

# Define the API URL
url = 'http://localhost:5000/send-slack-message'

# Define the JSON payload
payload = {
    "channel_name": "testing",
    "message": "this is a test"
}

# Set the Bearer token in headers
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer 2a3f5bcb-4bce-47b4-81e8-a4fdd4b8e0a5'  # Use the token from TOKENS dictionary
}

# Send the POST request
response = requests.post(url, headers=headers, data=json.dumps(payload))

if response.status_code == 200:
    print("Message sent successfully!")
    print("Response:", response.json())
else:
    print(f"Failed to send message. Status code: {response.status_code}")
    print("Response:", response.json())
