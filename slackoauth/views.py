from django.http import HttpResponse
from django.utils.http import urlencode
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
            slack_team, _ = SlackTeam.objects.get_or_create(
                team_id=r_json.get('team_id'),
            )
            slack_team.access_token = r_json.get('access_token')
            slack_team.save()

    if request.GET.get('error'):
        pass

    return HttpResponse('Thanks for adding the Infusionsoft Support Slackbot!')
