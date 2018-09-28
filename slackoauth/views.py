from django.http import HttpResponse
from django.utils.http import urlencode
import json
import os
import requests

from .models import SlackTeam


def auth(request):
    if request.GET.get('code'):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        uri = 'https://infusionsoftsupportslackbot.herokuapp.com/oauth/'
        data = urlencode({
            'client_id': os.environ['SLACK_CLIENT_ID'],
            'client_secret': os.environ['SLACK_CLIENT_SECRET'],
            'code': request.GET.get('code'),
            'redirect_uri': uri,
        })
        base_url = 'https://slack.com/api/oauth.access'
        url = base_url + '?' + data
        print(url)
        response = requests.post(url, headers=headers)
        print(response, response.reason)
        r_json = response.json()
        print(r_json)
        if r_json.get('access_token'):
            SlackTeam.objects.get_or_create(
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
