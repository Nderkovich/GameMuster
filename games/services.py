from django.conf import settings

from game_app.igdb_api import IGDBClient


def get_user_favorite_games(user):
    api_client = IGDBClient(settings.IGDB_API_KEY, settings.IGDB_API_URL)
    ids = []
    for g in user.favorite_games.all():
        ids.append(g.game_id)
    if ids:
        return api_client.get_games_by_ids(ids)
    else:
        return None
