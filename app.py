import os
import logging
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from onboarding_tutorial import OnboardingTutorial
import json
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__)

# Initialize a Flask app to host the events adapter
slack_events_adapter = SlackEventAdapter(os.environ['SLACK_SIGNING_SECRET'], "/slack/events", app)

#Initialize a web API client
slack_web_client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

onboarding_tutorials_sent = {}

@slack_events_adapter.on("channel_created")
def new_channel(payload):

    event = payload.get("event", {})
    channel = event.get("channel")
    channel_name = channel.get("name")

    def start_onboardings(user_id: str, channel: str):

        onboarding_tutorial = OnboardingTutorial(channel)

        message = {'channel':"C018BA3SERK",'blocks': [{'type':'section','text':{'type':'mrkdwn','text':f'@here\na new channel: #{channel_name} was created!'}}]}
        response = slack_web_client.chat_postMessage(**message)

        onboarding_tutorial.timestamp = response["ts"]

        if channel not in onboarding_tutorials_sent:
            onboarding_tutorials_sent[channel] = {}
        onboarding_tutorials_sent[channel][user_id] = onboarding_tutorial


#Please put user_id & channel_id into below.
    return start_onboardings("", "")

if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    app.run(port=5000)
