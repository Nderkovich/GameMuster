from django.db import models

from profiles.models import Profile


class Game(models.Model):
    game_id = models.IntegerField()
    game_name = models.CharField(max_length=200)
    cover_url = models.URLField(null=True)
    user_rating = models.IntegerField(null=True)
    user_rating_count = models.IntegerField(null=True)
    critic_rating = models.IntegerField(null=True)
    critic_rating_count = models.IntegerField(null=True)
    game_description = models.TextField(null=True)
    game_release_date = models.DateField(null=True)
    user_profiles = models.ManyToManyField(Profile, related_name='favorite_games', null=True)


class Keyword(models.Model):
    keyword_id = models.IntegerField()
    keyword_name = models.CharField(max_length=100)
    game = models.ManyToManyField(Game, related_name='keywords')


class Genre(models.Model):
    genre_id = models.IntegerField()
    genre_name = models.CharField(max_length=100)
    game = models.ManyToManyField(Game, related_name='genres')


class Platform(models.Model):
    platform_id = models.IntegerField()
    platform_name = models.CharField(max_length=100)
    platform_abbreviation = models.CharField(max_length=20, null=True)
    game = models.ManyToManyField(Game, related_name='platforms')


class Screenshot(models.Model):
    screen_thumb_url = models.URLField()
    screen_big_url = models.URLField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='screenshots', null=True)
