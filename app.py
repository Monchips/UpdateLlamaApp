from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Load environment variables from .env file (for local use)
load_dotenv()

# Set up Flask
app = Flask(__name__)

# Initialize WebClient with your Slack bot token
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
client = WebClient(token=SLACK_BOT_TOKEN)

# Access the Bearer tokens from environment variables
TOKENS = {
    os.getenv('Esteban'): "Esteban",
    os.getenv('Renato'): "Renato",
    os.getenv('Diego'): "Diego",
    os.getenv('Roy'): "Roy",
    os.getenv('Estefano'): "Estefano",
    os.getenv('Ernesto'): "Ernesto",
    os.getenv('Willy'): "Willy",
    os.getenv('Brendon'): "Brendon",
    os.getenv('LATAM_AlertService'): "LATAM_AlertService",
    os.getenv('USER10_TOKEN'): "User10"
}

# Helper function to verify the Bearer token
def verify_token(token):
    if token and token.startswith("Bearer "):
        token = token.split(" ")[1]  # Remove "Bearer " prefix
        if token in TOKENS:
            return TOKENS[token]
    return None

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

# Test route to ensure the app is running
@app.route('/')
def home():
    return "Hello from Flask on Render!"

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
    channel_name = data.get('channel_name', 'testing')  # Default to 'testing' if no channel_name provided
    message_text = data.get('message', 'No message provided.')

    # Find the channel ID by name
    conversation_id = find_channel_id(channel_name)
    if not conversation_id:
        return jsonify({'error': f"Channel '{channel_name}' not found"}), 404

    # Send the message to the found channel ID
    result = client.chat_postMessage(
        channel=conversation_id,
        text=f"{user}: {message_text}"
    )

    # Return the result
    return jsonify({'result': result.data}), 200

# Run the Flask app
if __name__ == '__main__':
    # Get the port from Render's environment (Render sets it automatically)
    port = int(os.environ.get('PORT', 5000))  # Render automatically sets the port
    app.run(host='0.0.0.0', port=port)
