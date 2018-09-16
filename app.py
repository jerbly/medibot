"""Medibot is a Slack bot running serverlessly in AWS via Chalice. Questions are passed
to a machine learning classifier running in sci-kit learn. The SVM model is loaded on
demand from S3 allowing it to be updated without redeploying or bloating the bot."""

from chalice import Chalice, ForbiddenError
import os
from slackclient import SlackClient
from sklearn.externals import joblib
import boto3

SLACK_VERIFICATION_TOKEN = os.environ["SLACK_VERIFICATION_TOKEN"]
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
BUCKET = os.environ["BUCKET"]
MODEL_KEY = os.environ["MODEL_KEY"]

TMP_FILE = '/tmp/model.pkl'

clf = None

app = Chalice(app_name='medibot')

client = SlackClient(SLACK_BOT_TOKEN)

def load_model():
    # Only load the classifier model once when it's first needed
    global clf
    if not clf:
        boto3.resource('s3').Object(BUCKET, MODEL_KEY).download_file(TMP_FILE)
        clf = joblib.load(TMP_FILE)

def predict_team(question):
    return clf.predict([question])[0]

@app.route('/slack/events', methods=['POST'])
def slack_event():
    payload = app.current_request.json_body

    if payload['token'] != SLACK_VERIFICATION_TOKEN:
        raise ForbiddenError("Forbidden")

    if 'challenge' in payload:
        # Check for challenge and respond (https://api.slack.com/events/url_verification):
        return {'challenge': payload['challenge']}

    if 'X-Slack-Retry-Reason' in app.current_request.headers:
        # Ignore some slack retries because we're being slow (https://api.slack.com/events-api#errors)
        print("Ignoring Slack Retry: {}".format(app.current_request.headers['X-Slack-Retry-Reason']))
        return {'msg': 'OK'}

    event = payload['event']
    message_text = event.get('text').lower()
    if event.get("subtype") is None and event.get("bot_id") is None:
        channel = event["channel"]
        if "who" in message_text:
            load_model()
            message = "<@{}>, you should probably talk to someone in team {} about that.".format(event["user"], predict_team(message_text))
        else:
            message = "<@{}>, try asking me a question containing the word 'who'.".format(event["user"])
        client.api_call("chat.postMessage", channel=channel, text=message)

    return {'msg': 'OK'}