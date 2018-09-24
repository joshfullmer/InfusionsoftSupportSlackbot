import datetime
from django.http import HttpResponse
from django.utils.http import unquote
from django.views.decorators.csrf import csrf_exempt
import json
import re
from utils import gsheet, slack


@csrf_exempt
def walkup(request):
    body_decoded = request.body.decode('utf-8')

    # Parse Slack Response
    parsed_response = {}
    for keyvalue in body_decoded.split('&'):
        key, value = keyvalue.split('=')
        parsed_response[key] = unquote(value)
    text = parsed_response['text'].replace('+', ' ')

    # Check if Slack User was mentioned
    user_id = re.findall(r'@([^\|]+)\|', text)
    if user_id:
        person = slack.get_username(user_id[0])
        description = ' '.join(text.split()[1:])

    # If not, respond with an error message
    else:
        response_data = {
            'response_type': 'ephemeral',
            'text': 'Please use the format: "[@user] [description]"',
        }
        return HttpResponse(
            json.dumps(response_data),
            content_type='application/json')

    # Prepare data to add to Google Sheet
    now_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    gsheet_data = [
        now_str,
        slack.get_username(parsed_response['user_id']),
        person,
        description
    ]

    # Add to Google Sheet
    gs = gsheet.GSheet('1cUsX-KP7yqsqDw-SNS8AEVp8c4prvjxjgA_wejrPxVY')
    gs.add_row(gsheet_data)

    # HTTP Response to Slack
    response_data = {
        'response_type': 'ephemeral',
        'text': 'Walk up successfully recorded',
        'attachments': [
            {
                'text': text
            }
        ]
    }
    return HttpResponse(
        json.dumps(response_data),
        content_type='application/json')
