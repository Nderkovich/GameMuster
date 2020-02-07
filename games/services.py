from django.conf import settings
from django.db import transaction
from datetime import datetime

from games.igdb_api import IGDBClient
from games.models import Game, Keyword, Screenshot, Genre, Platform


def get_user_favorite_games(user):
    api_client = IGDBClient(settings.IGDB_API_KEY, settings.IGDB_API_URL)
    ids = [game.game_id for game in user.favorite_games.all()]
    if ids:
        return api_client.get_games_by_ids(ids)
    else:
        return None


class GameFetcher():
    @transaction.atomic
    def create_game(self, data):
        game, created = Game.objects.update_or_create(
            game_id=data['id'],
            game_name=data.get('name'),
            game_description=data.get('summary'),
            user_rating=int(data.get('rating', 0)),
            user_rating_count=data.get('rating_count', 0),
            critic_rating=int(data.get('aggregated_rating', 0)),
            critic_rating_count=data.get('aggregated_rating_count', 0),
        )
        if data.get('cover'):
            game.cover_url = data['cover']['url'].replace('thumb', 'cover_big')
        if data.get('first_release_date'):
            game.game_release_date = datetime.utcfromtimestamp(data['first_release_date'])
        if data.get('keywords'):
            for keyword in data['keywords']:
                game.keywords.add(self._get_keyword(keyword))
        if data.get('genres'):
            for genre in data['genres']:
                game.genres.add(self._get_genre(genre))
        if data.get('platforms'):
            for platform in data['platforms']:
                game.platforms.add(self._get_platform(platform))
        if data.get('screenshots'):
            for screen in data['screenshots']:
                game.screenshots.add(self._get_screenshot(screen))
        game.save()

    @transaction.atomic
    def _get_keyword(self, key_data: dict) -> Keyword:
        keyword, created = Keyword.objects.update_or_create(
            keyword_id=key_data['id'],
            keyword_name=key_data['name'],
        )
        return keyword

    @transaction.atomic
    def _get_genre(self, genre_data: dict) -> Genre:
        genre, created = Genre.objects.update_or_create(
            genre_id=genre_data['id'],
            genre_name=genre_data['name'],
        )
        return genre

    @transaction.atomic
    def _get_platform(self, platform_data: dict) -> Platform:
        platform, created = Platform.objects.update_or_create(
            platform_id=platform_data['id'],
            platform_name=platform_data.get('name'),
            platform_abbreviation=platform_data.get('abbreviation'),
        )
        return platform

    @transaction.atomic
    def _get_screenshot(self, screenshot_data) -> Screenshot:
        screenshot, created = Screenshot.objects.update_or_create(
            screen_thumb_url=screenshot_data['url'],
            screen_big_url=screenshot_data['url'].replace(
                't_thumb', 't_screenshot_big')
        )
        return screenshot
