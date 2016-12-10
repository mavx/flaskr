"""Wrapper for Slack's Web API to post messages to channel."""

from __future__ import print_function # Python 2/3 compatibility
import os
from slackclient import SlackClient

SLACK_TOKEN = os.environ['SLACK_TOKEN']

class Slacker(object):
    def __init__(self, botname):
        self.slack = SlackClient(SLACK_TOKEN)
        self.botname = botname

    def test(self):
        return self.slack.api_call('api.test')

    def list_channels(self):
        r = self.slack.api_call('channels.list')
        channels = r.get('channels')
        for c in channels:
            print(c.get('name'), '({})'.format(c.get('id')))

    def post(self, message, channel_id='random'):
        # Post a message
        try:
            return self.slack.api_call(
                'chat.postMessage',
                channel=channel_id,
                text=message,
                username=self.botname,
                icon_emoji=':robot_face:'
            )
        except Exception as e:
            print(e.message)
