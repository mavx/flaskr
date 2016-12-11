"""Wrapper for Slack's Web API to post messages to channel."""

from __future__ import print_function # Python 2/3 compatibility
import time
import os
from slackclient import SlackClient

SLACK_TOKEN = os.environ['SLACK_TOKEN']
BOT_ID = 'U3D9KDKJQ'
# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"

class Slacker(object):
    def __init__(self, botname=None):
        self.slack = SlackClient(SLACK_TOKEN)
        if botname is None:
            self.botname = 'nameless'
        else:
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
                text=message
                # username=self.botname,
                # icon_emoji=':robot_face:'
            )
        except Exception as e:
            print(e.message)


def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
               "* command with numbers, delimited by spaces."
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure...write some more code then I can do that!"
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == '__main__':
    slack_client = SlackClient(SLACK_TOKEN)
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while 1:
            content = slack_client.rtm_read()
            print(content)
            command, channel = parse_slack_output(content)
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
