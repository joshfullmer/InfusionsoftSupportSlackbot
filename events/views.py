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
                'Messages'
            )
            gs.add_row(data)
            return HttpResponse('')

    return HttpResponse('This page is for receiving events from Slack.')
