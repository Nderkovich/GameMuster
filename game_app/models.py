from django.db import models
from profiles_app.models import Profile


class Game(models.Model):
    game_id = models.IntegerField()
    user_profiles = models.ManyToManyField(Profile, related_name='favorite_games', null=True)
