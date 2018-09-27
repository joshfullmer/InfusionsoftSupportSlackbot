from django.http import HttpResponse
import json
import os
import requests

from .models import SlackTeam


def auth(request):
    if request.GET.get('code'):
        uri = 'https://infusionsoftsupportslackbot.herokuapp.com/oauth/'
        data = {
            'client_id': os.environ['SLACK_CLIENT_ID'],
            'client_secret': os.environ['SLACK_CLIENT_SECRET'],
            'code': request.GET.get('code'),
            'redirect_uri': uri
        }
        url = 'https://slack.com/api/oauth.access'
        response = requests.get(url, json=data)
        print(response.text)
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
