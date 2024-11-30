# これはslackのbotのテストファイルです

import requests
import json

# Slack Webhook URL
webhook_url = "https://hooks.slack.com/services/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"

def send_slack_message(message: str):
    """
    Sends a message to a Slack channel using an incoming webhook.
    
    Args:
        message (str): The message to send to the Slack channel.
    """
    headers = {'Content-Type': 'application/json'}
    payload = {
        "text": message
    }
    
    try:
        response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            print("Message sent successfully!")
        else:
            print(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    test_message = "Hello, Slack! This is a test message from your bot."
    send_slack_message(test_message)
