from django.db import models


class SlackTeam(models.Model):
    # TODO: add scope, user_id, team_name to model
    team_id = models.CharField(max_length=50)
    access_token = models.CharField(max_length=100)
