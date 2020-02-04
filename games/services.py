from django.conf import settings
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
    def create_game(self, data):
        if not Game.objects.filter(game_id=data['id']).exists():
            game = Game(game_id=data['id'])
            game.game_name = data.get('name')
            if data.get('cover'):
                game.cover_url = data['cover']['url'].replace('thumb', 'cover_big')
            game.game_description = data.get('summary')
            game.user_rating = int(data.get('rating', 0))
            game.user_rating_count = data.get('rating_count', 0)
            game.critic_rating = int(data.get('aggregated_rating', 0))
            game.critic_rating_count = data.get('aggregated_rating_count', 0)
            if data.get('first_release_date'):
                game.game_release_date = datetime.utcfromtimestamp(data['first_release_date'])
            game.save()
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

    def _get_keyword(self, key_data: dict) -> Keyword:
        if not Keyword.objects.filter(keyword_id=key_data['id']).exists():
            return self._create_keyword(key_data)
        else:
            return Keyword.objects.get(keyword_id=key_data['id'])

    def _create_keyword(self, key_data: dict) -> Keyword:
        keyword = Keyword(keyword_id=key_data['id'])
        keyword.Keyword_name = key_data['name']
        keyword.save()
        return keyword

    def _get_genre(self, genre_data: dict) -> Genre:
        if not Genre.objects.filter(genre_id=genre_data['id']).exists():
            return self._create_genre(genre_data)
        else:
            return Genre.objects.get(genre_id=genre_data['id'])

    def _create_genre(self, genre_data: dict) -> Genre:
        genre = Genre(genre_id=genre_data['id'])
        genre.genre_name = genre_data['name']
        genre.save()
        return genre

    def _get_platform(self, platform_data: dict) -> Platform:
        if not Platform.objects.filter(platform_id=platform_data['id']).exists():
            return self._create_platform(platform_data)
        else:
            return Platform.objects.get(platform_id=platform_data['id'])

    def _create_platform(self, platform_data: dict) -> Platform:
        platform = Platform(platform_id=platform_data['id'])
        platform.platform_name = platform_data.get('name')
        platform.platform_abbreviation = platform_data.get('abbreviation')
        platform.save()
        return platform

    def _get_screenshot(self, screenshot_data) -> Screenshot:
        if not Screenshot.objects.filter(screen_thumb_url=screenshot_data['url']).exists():
            return self._create_screenshot(screenshot_data)
        else:
            return Screenshot.objects.get(screen_thumb_url=screenshot_data['url'])

    def _create_screenshot(self, screenshot_data: dict) -> Screenshot:
        screen = Screenshot(screen_thumb_url=screenshot_data['url'])
        screen.screen_big_url = screen.screen_thumb_url.replace(
            't_thumb', 't_screenshot_big')
        screen.save()
        return screen
