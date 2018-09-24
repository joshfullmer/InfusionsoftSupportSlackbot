import datetime
from django.http import HttpResponse
from django.utils.http import unquote
from django.views.decorators.csrf import csrf_exempt
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
import os
import re
from utils import gsheet, slack


@csrf_exempt
def walkup(request):
    body_decoded = request.body.decode('utf-8')
    parsed_response = {}
    for keyvalue in body_decoded.split('&'):
        key, value = keyvalue.split('=')
        parsed_response[key] = unquote(value)
    text = parsed_response['text'].replace('+', ' ')
    user_id = re.findall(r'@([^\|]+)\|', text)
    if user_id:
        person = slack.get_username(user_id[0])
        description = ' '.join(text.split()[1:-1])
    else:
        response_data = {
            'response_type': 'ephemeral',
            'text': 'Please use the format: "[@user] [description]"',
        }
        return HttpResponse(
            response_data,
            content_type='application/json')
    now_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    gsheet_data = [
        now_str,
        slack.get_username(parsed_response['user_id']),
        person,
        description
    ]
    gs = gsheet.GSheet('1cUsX-KP7yqsqDw-SNS8AEVp8c4prvjxjgA_wejrPxVY')
    gs.add_row(gsheet_data)
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


def gsheet_test(request):
    scopes = ['https://spreadsheets.google.com/feeds',
              'https://www.googleapis.com/auth/drive']

    cred_dict = json.loads(os.environ['CREDS'], strict=False)

    credentials = ServiceAccountCredentials.from_json_keyfile_dict(
        cred_dict,
        scopes=scopes)

    gc = gspread.authorize(credentials)

    spreadsheet_key = '1cUsX-KP7yqsqDw-SNS8AEVp8c4prvjxjgA_wejrPxVY'

    spreadsheet = gc.open_by_key(spreadsheet_key)

    worksheet = spreadsheet.sheet1

    now_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    worksheet.append_row(['Me', now_str])

    print(worksheet.get_all_records())
