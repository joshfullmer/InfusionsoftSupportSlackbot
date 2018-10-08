import datetime as dt
from pytz import timezone, utc
import re
import requests
from urllib.parse import urlencode


from slackoauth.models import SlackTeam
from utils.categorize import categorize


SLACK_OAUTH_TOKEN = ('xoxp-437909661060-439459703494-437913616996-'
                     'da335ca2ffc505ab2c504bfd8cea6e92')

headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

SLACK_API_URL = 'https://slack.com/api/'


def get_username(team_id, user_id):
    url = SLACK_API_URL
    url += 'users.profile.get'
    params = urlencode({
        'token': SlackTeam.get_token(team_id),
        'user': user_id,
    })
    url = url + '?' + params
    response = requests.get(url, headers=headers)
    r_json = response.json()
    username = r_json.get('profile').get('real_name')
    return username


def get_channel_name(team_id, channel_id):
    url = SLACK_API_URL
    url += 'channels.info'
    params = urlencode({
        'token': SlackTeam.get_token(team_id),
        'channel': channel_id,
    })
    url = url + '?' + params
    response = requests.get(url, headers=headers)
    r_json = response.json()
    channel_name = r_json.get('channel').get('name')
    return channel_name


def parse_message(message, team_id):
    if message.get('message'):
        message = message.get('message')
    parent_message_id = message.get('thread_ts')
    if not parent_message_id:
        previous_message = message.get('previous_message')
        if previous_message:
            parent_message_id = previous_message.get('thread_ts')
    message_id = message.get('ts')

    ts = float(message.get('ts'))

    arizona = timezone('US/Arizona')
    ts_dt = dt.datetime.fromtimestamp(ts)
    ts_dt_utc = utc.localize(ts_dt)
    ts_dt_az = ts_dt_utc.astimezone(arizona)

    ts_str = ts_dt_az.strftime('%Y-%m-%d %H:%M:%S')

    user = message.get('user')

    if user:
        username = get_username(team_id, message.get('user'))
    else:
        username = None

    text = message.get('text')

    if text:
        matches = re.findall(r'<@(.*?)>', text)

        if matches:
            repl = {}
            for match in matches:
                repl[match] = get_username(team_id, match)
            for user_id, user in repl.items():
                text = text.replace(f'<@{user_id}>', user)

    if parent_message_id and not parent_message_id == message_id:
        data = [
            message_id,
            ts_str,
            parent_message_id,
            username,
            text,
        ]
        tab = 'Replies'
    else:
        has_replies = False
        categories = categorize(text) if text else None
        data = [
            message_id,
            ts_str,
            username,
            text,
            has_replies,
            categories,
        ]
        tab = 'Messages'

    if message.get('deleted_ts'):
        data = [message.get('deleted_ts')]
    return data, tab
