# Generated by Django 2.1.1 on 2018-09-28 00:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('slackoauth', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='slackteam',
            name='refresh_token',
        ),
    ]