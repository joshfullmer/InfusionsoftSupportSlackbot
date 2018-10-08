import datetime as dt
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from pytz import timezone, utc
import os
import re

from utils.categorize import categorize
from utils.gsheet import GSheet
from utils.slack import get_username, get_channel_name

SKIP_SUBTYPES = [
    'bot_message',
    'channel_archive',
    'channel_join',
    'channel_leave',
    'channel_name',
    'channel_purpose',
    'channel_topic',
    'channel_unarchive',
    'file_comment',
    'file_mention',
    'file_share',
    'group_archive',
    'group_join',
    'group_leave',
    'group_name',
    'group_purpose',
    'group_topic',
    'group_unarchive',
    'me_message',
    'message_changed',
    'message_deleted',
    'message_replied',
    'pinned_item',
    'reply_broadcast',
    'thread_broadcast',
    'unpinned_item'
]


@csrf_exempt
def event(request):
    body = json.loads(request.body)
    print(body)
    challenge = body.get('challenge')
    if challenge:
        return HttpResponse(
            json.dumps({'challenge': challenge}),
            content_type='application/json',
        )

    team_id = body.get('team_id')

    # Checks if post is valid, coming from Slack

    if body.get('token') == os.environ['SLACK_VERIFICATION_TOKEN']:
        message = body.get('event')
        subtype = message.get('subtype')

        if subtype:
            # TODO handle when messages are deleted or edited
            return HttpResponse('')

        channel_name = get_channel_name(team_id, message.get('channel'))
        if channel_name == 'customersupport':

            message_id = message.get('ts')

            ts = float(message.get('ts'))

            arizona = timezone('US/Arizona')
            ts_dt = dt.datetime.fromtimestamp(ts)
            ts_dt_utc = utc.localize(ts_dt)
            ts_dt_az = ts_dt_utc.astimezone(arizona)

            ts_str = ts_dt_az.strftime('%Y-%m-%d %H:%M:%S')

            username = get_username(team_id, message.get('user'))

            text = message.get('text')

            matches = re.findall(r'<@(.*?)>', text)

            if matches:
                repl = {}
                for match in matches:
                    repl[match] = get_username(team_id, match)
                for user_id, user in repl.items():
                    text = text.replace(f'<@{user_id}>', user)

            has_replies = False

            categories = categorize(text)

            if message.get('thread_ts'):
                data = [
                    message_id,
                    ts_str,
                    message.get('thread_ts'),
                    username,
                    text
                ]
                tab = 'Replies'
            else:
                data = [
                    message_id,
                    ts_str,
                    username,
                    text,
                    has_replies,
                    categories,
                ]
                tab = 'Messages'

            gs = GSheet(
                '1heNDfpCkgHF-CPUJFbFAc0Us9I_BWde1KrFU9yaVowc',
                tab
            )
            gs.add_row(data)
            return HttpResponse('')

    return HttpResponse('This page is for receiving events from Slack.')
