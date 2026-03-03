from flask import Flask, jsonify
import logging
import boto3
import os
from watchtower import CloudWatchLogHandler
import time

app = Flask(__name__)

# Configure S3 logging
S3_BUCKET = os.getenv('S3_BUCKET_NAME', 'devops-mini-app-logs')
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
ENABLE_S3_LOGGING = os.getenv('ENABLE_S3_LOGGING', 'false').lower() == 'true'

# Setup logging
logger = logging.getLogger('devops-app')
logger.setLevel(logging.INFO)

# Console handler (always enabled)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

# S3/CloudWatch handler (optional)
if ENABLE_S3_LOGGING:
    try:
        # CloudWatch Logs Handler (logs go to CloudWatch, can be exported to S3)
        cw_handler = CloudWatchLogHandler(
            log_group='/devops-mini-app',
            stream_name=f'app-{int(time.time())}',
            boto3_client=boto3.client('logs', region_name=AWS_REGION)
        )
        cw_handler.setLevel(logging.INFO)
        logger.addHandler(cw_handler)
        logger.info('CloudWatch logging enabled - logs can be exported to S3')
    except Exception as e:
        logger.warning(f'CloudWatch logging disabled: {str(e)}')

@app.route("/")
def home():
    logger.info('Home endpoint accessed')
    return "Hello from DevOps on AWS 🚀 (with S3 Logging) - Auto-Deployed via GitHub Actions!"

@app.route("/health")
def health():
    logger.info('Health check endpoint accessed')
    return {"status": "healthy", "s3_logging": ENABLE_S3_LOGGING}, 200

@app.route("/test-log")
def test_log():
    logger.info('Test log entry created')
    logger.warning('This is a warning log')
    logger.error('This is an error log for testing')
    return {"message": "Logs sent", "s3_enabled": ENABLE_S3_LOGGING}, 200

@app.route("/users")
def users():
    """Return a list of sample users"""
    logger.info('Users endpoint accessed')
    sample_users = [
        {"id": 1, "name": "Alice", "role": "Developer"},
        {"id": 2, "name": "Bob", "role": "DevOps Engineer"},
        {"id": 3, "name": "Charlie", "role": "System Admin"}
    ]
    return jsonify(sample_users)

if __name__ == "__main__":
    logger.info('Starting DevOps Mini App...')
    app.run(host="0.0.0.0", port=5000)
