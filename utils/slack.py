import requests
from urllib.parse import urlencode


SLACK_OAUTH_TOKEN = ('xoxp-437909661060-439459703494-437913616996-'
                     'da335ca2ffc505ab2c504bfd8cea6e92')

headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

SLACK_API_URL = 'https://slack.com/api/'


def get_username(user_id):
    url = SLACK_API_URL
    url += 'users.profile.get'
    params = urlencode({
        'token': SLACK_OAUTH_TOKEN,
        'user': user_id,
    })
    url = url + '?' + params
    response = requests.get(url, headers=headers)
    r_json = response.json()
    username = r_json.get('profile').get('real_name')
    return username
