from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os

from utils.gsheet import GSheet
from utils.slack import get_channel_name, parse_message

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

        channel_name = get_channel_name(team_id, message.get('channel'))
        if channel_name == 'customersupport':

            data, tab = parse_message(message, team_id)

            gs = GSheet(
                '1heNDfpCkgHF-CPUJFbFAc0Us9I_BWde1KrFU9yaVowc',
                tab
            )

            if subtype:
                # TODO handle when messages are deleted or edited
                if subtype == 'message_changed':
                    gs.update_message(data)
                if subtype == 'message_deleted':
                    gs.delete_message(data)
            else:
                gs.add_message(data)
            return HttpResponse('')

    return HttpResponse('This page is for receiving events from Slack.')
