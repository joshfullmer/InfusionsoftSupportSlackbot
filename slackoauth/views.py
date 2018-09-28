from django.http import HttpResponse
import json
import os
import requests

from .models import SlackTeam


def auth(request):
    if request.GET.get('code'):
        uri = ('https%3A%2F%2Finfusionsoftsupportslackbot'
               '.herokuapp.com%2Foauth%2F')
        data = {
            'client_id': os.environ['SLACK_CLIENT_ID'],
            'client_secret': os.environ['SLACK_CLIENT_SECRET'],
            'code': request.GET.get('code'),
        }
        url = 'https://slack.com/api/oauth.access'
        response = requests.post(url, json=data)
        print(response, response.reason)
        if response.status_code == 403:
            return HttpResponse(response.text)
        r_json = response.json()
        if r_json.get('access_token'):
            SlackTeam.object.get_or_create(
                team_id=request.GET.get('team_id'),
                access_token=r_json.get('access_token'),
                refresh_token=r_json.get('refresh_token'),
            )

    if request.GET.get('error'):
        pass

    response_data = {}
    return HttpResponse(
        json.dumps(response_data),
        content_type='application/json')
