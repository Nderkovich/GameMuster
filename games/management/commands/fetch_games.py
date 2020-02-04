from django.core.management.base import BaseCommand
from django.conf import settings
from celery import group

from games.igdb_api import IGDBClient
from games.tasks import game_getter_task


class Command(BaseCommand):
    api_client = IGDBClient(settings.IGDB_API_KEY, settings.IGDB_API_URL)

    def add_arguments(self, parser):
        parser.add_argument('offset', type=int, help="Game offset")
        parser.add_argument('limit', type=int, help="Number of games to get")

    def get_games(self, offset=0, limit=500):
        call_group = []
        while offset < 1000:
            call_group.append(game_getter_task.s(offset, limit))
            offset += 500
        lazy_group = group(call_group)
        lazy_group()

    def handle(self, *args, **options):
        self.get_games(options['offset'], options['limit'])
