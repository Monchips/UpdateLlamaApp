from flask import Flask, request, jsonify
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

load_dotenv()
# Set up Flask
app = Flask(__name__)

# Initialize WebClient with your token
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
client = WebClient(token=SLACK_BOT_TOKEN)

# Predefined tokens and their associated users
TOKENS = {
    "2a3f5bcb-4bce-47b4-81e8-a4fdd4b8e0a5": "Esteban",
    "7e16d90e-3e8d-4786-bd4e-bf4971adfd2e": "Renato",
    "5e5d8e8b-7a1e-4fb2-8c21-68b7032f89f3": "Willfredo",
    "8c6f8884-7495-46a0-84a2-f8a25731d751": "Brendon",
    "88b94fe4-3c1a-4429-a027-7d40afed640b": "User5",
    "c61b27c6-4216-492a-82d9-37f246fc99ad": "User6",
    "3af8d321-c09d-4c60-8434-b389a9fa5d37": "User7",
    "f23b1a4c-2e97-4b92-86d4-1e5b07f65b18": "User8",
    "97d3b2d2-0a8b-4be5-8c14-2b1d303ef3be": "User9",
    "e05a1fc9-1129-4ecb-a732-469d73cf96b3": "User10"
}

# Helper function to find a channel ID by name
def find_channel_id(channel_name):
    response = client.conversations_list(limit=100, types="public_channel,private_channel")
    channels = response['channels']
    while response.get('response_metadata', {}).get('next_cursor'):
        response = client.conversations_list(cursor=response['response_metadata']['next_cursor'], types="public_channel,private_channel")
        channels.extend(response['channels'])

    for channel in channels:
        if channel["name"] == channel_name:
            return channel["id"]
    return None

# Helper function to verify the Bearer token
def verify_token(token):
    # Remove the "Bearer " prefix and check if the token exists in the TOKENS dict
    if token and token.startswith("Bearer "):
        token = token.split(" ")[1]
        if token in TOKENS:
            return TOKENS[token]
    return None

# Route to handle incoming JSON data and post message to Slack
@app.route('/send-slack-message', methods=['POST'])
def send_slack_message():
    # Get the Authorization header
    auth_header = request.headers.get('Authorization')
    
    # Verify the token
    user = verify_token(auth_header)
    if not user:
        return jsonify({'error': 'Unauthorized access'}), 401

    # Extract message details from the request
    data = request.json
    channel_name = data.get('channel_name', 'testing')
    message_text = data.get('message', 'No message provided.')

    # Find the channel ID by name
    conversation_id = find_channel_id(channel_name)
    if not conversation_id:
        return jsonify({'error': f"Channel '{channel_name}' not found"}), 404

    # Send the message to the found channel ID
    result = client.chat_postMessage(
        channel=conversation_id,
        text=f"{user}: {message_text}"  # Optionally include the user's name in the message
    )

    # Return the result
    return jsonify({'result': result.data}), 200

# Run the Flask app
if __name__ == '__main__':
    app.run(port=5000, debug=True)
