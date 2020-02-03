from django.conf import settings

from games.igdb_api import IGDBClient


def get_user_favorite_games(user):
    api_client = IGDBClient(settings.IGDB_API_KEY, settings.IGDB_API_URL)
    ids = [game.game_id for game in user.favorite_games.all()]
    if ids:
        return api_client.get_games_by_ids(ids)
    else:
        return None
