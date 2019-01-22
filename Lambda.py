"""Listener module."""
import sys
import json
from botocore.vendored import requests
import random
import os
from pprint import pprint

#Use lambda enviroment variables (if you intend to version it)
#ZOOM_INCOMING_WH_URL = Url of incoming webhook
#ZOOM_INCOMING_WH_PW  = Password of the hook

webhook_url = os.environ['ZOOM_INCOMING_WH_URL']

def pull_request_create(data):
    title = "Pull Request created!"
    summary = "Pull Request \"" + data['pullrequest']['title'] + "\"\nPor " + \
              data['pullrequest']['author']['display_name'] + " foi criado!"
    body = "Reviewers for this Pullreques:\n"

    for reviewer in data['pullrequest']['reviewers']:
        body += reviewer['display_name'] + '\n'

    body += "\nLink: " + data['pullrequest']['links']['html']['href']
    return title, summary, body


def pull_request_approve(data):
    title = "New approval!"
    summary = "Pull request \"" + data['pullrequest']['title'] + "\" was approved by " + \
              data['approval']['user']['display_name'] + "!!"
    body = "\nLink: " + data['pullrequest']['links']['html']['href']

    return title, summary, body


def pull_request_merge(data):
    title = "Pull Request Merged"
    summary = "Pull request \"" + data['pullrequest']['title'] + "\" was MERGED"
    body = "\nLink: " + data['pullrequest']['links']['html']['href']

    return title, summary, body


def pull_request_comment(data):
    title = "New comment!"
    summary = "New Comment on \"" + data['pullrequest']['title'] + "\" Pull Request!"
    body = data['comment']['content']['raw']
    body += "\nLink: " + data['pullrequest']['links']['html']['href']

    return title, summary, body


def lambda_handler(event, context):
    if event['method'] == "POST":
        if 'X-Event-Key' in event['headers']:
            data = event['body']
            # these values you find on bitbucket documentation
            if event['headers']['X-Event-Key'] == 'pullrequest:approved':
                title, summary, body = pull_request_approve(data)

            if event['headers']['X-Event-Key'] == 'pullrequest:fulfilled':
                title, summary, body = pull_request_merge(data)

            if event['headers']['X-Event-Key'] == 'pullrequest:comment_created':
                title, summary, body = pull_request_comment(data)

            if event['headers']['X-Event-Key'] == 'pullrequest:created':
                title, summary, body = pull_request_create(data)

            zoom_data = {
                "title": title,
                "summary": summary,
                "body": body
            }

            response = requests.post(
                webhook_url, data=json.dumps(zoom_data),
                headers={'Accept': 'application/json, application/xml',
                         'Content-Type': 'application/json',
                         'X-Zoom-Token': os.environ['ZOOM_INCOMING_WH_PW']}
            )

            if response.status_code != 200:
                print("Error " + response.status_code + " [RESPONSE] " + response.text)
            return "Message received"
        else:
            return "Invalid header"
    else:
        return "NOO"


