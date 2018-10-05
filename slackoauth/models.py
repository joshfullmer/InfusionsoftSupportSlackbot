from django.db import models


class SlackTeam(models.Model):
    # TODO: add scope, user_id, team_name to model
    team_id = models.CharField(max_length=50)
    access_token = models.CharField(max_length=100)

    @classmethod
    def get_token(cls, team_id):
        try:
            slack_team = SlackTeam.objects.get(team_id=team_id)
        except SlackTeam.DoesNotExist:
            slack_team = None
        if slack_team:
            return slack_team.access_token
        else:
            return None
