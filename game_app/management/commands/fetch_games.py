from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from game_app.igdb_api import IGDBClient
from game_app.models import Game, Genre, Screenshot, Keyword, Platform


class Command(BaseCommand):
    api_client = IGDBClient(settings.IGDB_API_KEY, settings.IGDB_API_URL)

    def get_games(self, offset=0, limit=9):
        game_list = self.api_client.get_game_list_full_data(offset, limit)
        for game in game_list:
            self.create_game(game)

    def handle(self, *args, **options):
        self.get_games()

    def create_game(self, data):
        if not Game.objects.filter(game_id=data['id']).exists():
            game = Game(game_id=data['id'])
        else:
            game = Game.objects.get(game_id=data['id'])
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
                game.keywords.add(self.create_keyword(keyword))
        if data.get('genres'):
            for genre in data['genres']:
                game.genres.add(self.create_genre(genre))
        if data.get('platforms'):
            for platform in data['platforms']:
                game.platforms.add(self.create_platform(platform))
        if data.get('screenshots'):
            for screen in data['screenshots']:
                game.screenshots.add(self.create_screenshot(screen))
        game.save()

    def create_keyword(self, key_data):
        if not Keyword.objects.filter(keyword_id=key_data['id']).exists():
            keyword = Keyword(keyword_id=key_data['id'])
            keyword.Keyword_name = key_data['name']
            keyword.save()
        else:
            keyword = Keyword.objects.get(keyword_id=key_data['id'])
        return keyword

    def create_genre(self, genre_data):
        if not Genre.objects.filter(genre_id=genre_data['id']).exists():
            genre = Genre(genre_id=genre_data['id'])
            genre.genre_name = genre_data['name']
            genre.save()
        else:
            genre = Genre.objects.get(genre_id=genre_data['id'])
        return genre

    def create_platform(self, platform_data):
        if not Platform.objects.filter(platform_id=platform_data['id']).exists():
            platform = Platform(platform_id=platform_data['id'])
            platform.platform_name = platform_data.get('name')
            platform.platform_abbreviation = platform_data.get('abbreviation')
            platform.save()
        else:
            platform = Platform.objects.get(platform_id=platform_data['id'])
        return platform

    def create_screenshot(self, screenhsot):
        if not Screenshot.objects.filter(screen_thumb_url=screenhsot['url']).exists():
            screen = Screenshot(screen_thumb_url=screenhsot['url'])
            screen.screen_big_url = screen.screen_thumb_url.replace(
                't_thumb', 't_screenshot_big')
            screen.save()
        else:
            screen = Screenshot.objects.get(screen_thumb_url=screenhsot['url'])
        return screen
