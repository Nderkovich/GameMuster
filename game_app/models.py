from django.db import models
from django.contrib.auth.models import AbstractUser


class Profile(AbstractUser):
    birthday = models.DateField(null=True)

    def is_in_favorite(self, game_id):
        if self.favorite_games.all().filter(game_id=game_id):
            return True
        return False


class Game(models.Model):
    game_id = models.IntegerField()
    user_profiles = models.ManyToManyField(Profile, related_name='favorite_games', null=True)
