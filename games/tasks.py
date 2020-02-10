from celery.schedules import crontab
from celery.task import periodic_task, task
from celery.utils.log import get_task_logger
from django.core import management
from django.conf import settings

from games.igdb_api import IGDBClient
from games.services import GameCreator

logger = get_task_logger(__name__)

START_OFFSET = 0
MAX_LIMIT = 500


@periodic_task(run_every=(crontab(hour='*/12')), name="game_fetcher")
def game_fetch_task():
    management.call_command("fetch_games", START_OFFSET, MAX_LIMIT)


@task()
def game_getter_task(offset, limit):
    game_fetcher = GameCreator()
    api_client = IGDBClient(settings.IGDB_API_KEY, settings.IGDB_API_URL)
    game_list = api_client.get_game_list_full_data(offset, limit)
    for game in game_list:
        game_fetcher.create_game(game)
    logger.info(f"Game {offset} - {offset + limit}")
