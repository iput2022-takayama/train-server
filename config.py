import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL', 'your_default_webhook_url')
    DEBUG = True
