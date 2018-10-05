import datetime as dt
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
import re

from utils.categorize import categorize
from utils.gsheet import GSheet
from utils.slack import get_username


@csrf_exempt
def event(request):
    body = json.loads(request.body)
    challenge = body.get('challenge')
    if challenge:
        return HttpResponse(
            json.dumps({'challenge': challenge}),
            content_type='application/json',
        )

    # Checks if post is valid, coming from Slack

    if body.get('token') == os.environ['SLACK_VERIFICATION_TOKEN']:
        message = body.get('event')
        message_id = message.get('ts')

        ts = float(message.get('ts'))
        ts_dt = dt.datetime.fromtimestamp(ts)
        ts_str = ts_dt.strftime('%Y-%m-%d %H:%M:S')

        team_id = body.get('team_id')
        username = get_username(team_id, message.get('user'))

        matches = re.findall(r'<@(.*?)>', message.get('text'))

        text = message.get('text')

        if matches:
            repl = {}
            for match in matches:
                repl[match] = get_username(team_id, match)
            for user_id, user in repl.items():
                text = text.replace(f'<@{user_id}>', user)

        has_replies = False

        categories = categorize(text)

        data = [
            message_id,
            ts_str,
            username,
            text,
            has_replies,
            categories,
        ]

        gs = GSheet(
            '1heNDfpCkgHF-CPUJFbFAc0Us9I_BWde1KrFU9yaVowc',
            'Message'
        )
        gs.add_row(data)
        return HttpResponse('')

    return HttpResponse('This page is for receiving events from Slack.')
