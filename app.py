from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Load environment variables from .env file
load_dotenv()

# Set up Flask
app = Flask(__name__)

# Initialize WebClient with your Slack bot token
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
client = WebClient(token=SLACK_BOT_TOKEN)

# Access the Bearer tokens from environment variables
TOKENS = {
    os.getenv('USER1_TOKEN'): "Esteban",
    os.getenv('USER2_TOKEN'): "Renato",
    os.getenv('USER3_TOKEN'): "User3",
    os.getenv('USER4_TOKEN'): "User4",
    os.getenv('USER5_TOKEN'): "User5",
    os.getenv('USER6_TOKEN'): "User6",
    os.getenv('USER7_TOKEN'): "User7",
    os.getenv('USER8_TOKEN'): "User8",
    os.getenv('USER9_TOKEN'): "User9",
    os.getenv('USER10_TOKEN'): "User10"
}

# Helper function to verify the Bearer token
def verify_token(token):
    if token and token.startswith("Bearer "):
        token = token.split(" ")[1]  # Remove "Bearer " prefix
        if token in TOKENS:
            return TOKENS[token]
    return None

# Flask route to handle incoming JSON data and post message to Slack
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
        text=f"{user} says: {message_text}"
    )

    # Return the result
    return jsonify({'result': result.data}), 200

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

# Run the Flask app
if __name__ == '__main__':
    app.run(port=5000, debug=True)
