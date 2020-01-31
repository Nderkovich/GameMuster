from django.db import models
from django.contrib.auth.models import AbstractUser


class Profile(AbstractUser):
    birthday = models.DateField(null=True)

    def is_in_favorite(self, game_id):
        return self.favorite_games.all().filter(game_id=game_id).exists()
