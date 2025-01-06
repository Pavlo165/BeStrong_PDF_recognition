import logging
import os
import json
from azure.functions import InputStream
from slack_sdk import WebClient
import requests

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_BOT_USERNAME = os.getenv("SLACK_BOT_USERNAME")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DISCORD_CHANNEL = os.getenv("DISCORD_CHANNEL")

def main(mainBlob: InputStream):
    message = f"The newly processed file *{mainBlob.name}* has been added to the archive."
    if not all([SLACK_BOT_TOKEN, SLACK_BOT_USERNAME, SLACK_CHANNEL]):
        logging.error("Missing required environment variables for sending push to Slack.")
    else:
        client = WebClient(token=SLACK_BOT_TOKEN)
        client.chat_postMessage(
            channel=SLACK_CHANNEL,
            text=message, 
            username=SLACK_BOT_USERNAME
        )
    
    if not all([DISCORD_BOT_TOKEN, DISCORD_CHANNEL]):
        logging.error("Missing required environment variables for sending push to Discord.")
    else:   # https://discord.com/developers/docs/resources/message#create-message
        url = f"https://discord.com/api/v10/channels/{DISCORD_CHANNEL}/messages"
        headers = {
            "Authorization": f"Bot {DISCORD_BOT_TOKEN}",
            "Content-Type": "application/json"
        }
        data = {
            "content": message
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            logging.error(f"Failed to send message: {response.status_code}\t{response.text}")