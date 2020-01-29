from django.db import models
from django.contrib.auth.models import AbstractUser


class Profile(AbstractUser):
    birthday = models.DateField(null=True)


class Game(models.Model):
    game_id = models.IntegerField()
    user_profiles = models.ManyToManyField(Profile, related_name='favorite_games', null=True)
