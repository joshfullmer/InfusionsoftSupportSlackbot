from django.http import HttpResponse
from django.utils.http import unquote
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def slash(request):
    body_decoded = request.body.decode('utf-8')
    parsed_response = {}
    for keyvalue in body_decoded.split('&'):
        key, value = keyvalue.split('=')
        parsed_response[key] = unquote(value)
    response_data = {
        'response_type': 'ephemeral',
        'text': 'Walk up successfully recorded',
        'attachments': [
            {
                'text': parsed_response['text']
            }
        ]
    }
    return HttpResponse(
        json.dumps(response_data),
        content_type='application/json')
