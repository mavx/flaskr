"""Wrapper for Slack's Web API to post messages to channel."""

from __future__ import print_function # Python 2/3 compatibility
import datetime as dt
import time
import os
import re
from slackclient import SlackClient

READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
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


def handle_command(client, command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
               "* command with numbers, delimited by spaces."
    if command.lower().startswith('do'):
        response = "Sure...write some more code then I can do that!"
    elif command.lower().startswith('user'):
        sql = parse(command)
        response = query(sql)[1][0]
    elif command.lower().startswith('query'):
        sql = command.replace('query', '')
        response = query(sql)
    client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def query(sql_statement):
    """Sends SQL statement to DB and returns results"""
    import psql

    def parse(value):
        try:
            return str(value)
        except Exception as e:
            print(e.message)
            return value

    db = psql.Connection()
    try:
        results = db.execute(sql_statement)
        return str(results)
        # return [[parse(val) for val in row] for row in results]
    except:
        db.rollback()
        return None


def parse_date(date):
    pass
    
def parse(string):
    """Parses message input into SQL statements
    Example:
        - What is GB for today?
        - How many users do we have on fave android today?
    """

    """
    [metric][date_range]
    
    """
    # Patterns
    re_all_brackets = r'\[.*?\]'
    re_single_date = r'\[\d{4}-\d{2}-\d{2}\]'
    re_date_range = r'\[\d{4}-\d{2}-\d{2}, \d{4}-\d{2}-\d{2}\]'
    re_metric = r'\[\w+\]'

    args = re.findall(re_all_brackets, string)
    metric = re.findall(re_metric, string)
    single_date = re.findall(re_single_date, string)
    date_range = re.findall(re_date_range, string)

    # if len(args) = 2:
    #     if metric and (single_date or date_range):
    #         metric = metric[0].replace('[', '').replace(']', '')
    #         if single_date:
    #             date = single_date[0].replace('[', '').replace(']', '')
    #         elif date_range:
    #             date = date_range[0].replace('[', '').replace(']', '')

    # else:
    #     feedback = "I don't understand."

    


    sql = """
    select sum(users) from bi_dwh.external_localytics
    where date='{}'
    and newuser='NA'
    """.format(dt.date.today())

    return sql


def main():
    slack_client = SlackClient(SLACK_TOKEN)
    if slack_client.rtm_connect():
        print("Bot ({}) connected and running!".format(BOT_ID))
        while 1:
            content = slack_client.rtm_read()
            print(content)
            command, channel = parse_slack_output(content)
            if command and channel:
                handle_command(slack_client, command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
    

if __name__ == '__main__':
    main()
