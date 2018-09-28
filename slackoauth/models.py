from django.db import models


class SlackTeam(models.Model):
    team_id = models.CharField(max_length=50)
    access_token = models.CharField(max_length=100)
