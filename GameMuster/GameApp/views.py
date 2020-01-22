from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.conf import settings


from .igdb_api import IGDBClient
from .twitter_api import TwitterApi


def mainpage(request: HttpRequest) -> HttpResponse:
    return render(request, 'Games/list.html')


def detailpage(request: HttpRequest) -> HttpResponse:
    return render(request, 'Games/info.html')


def list_test(request):
    api_client = IGDBClient(settings.IGDB_API_KEY, settings.IGDB_API_URL)
    game_list = api_client.get_game_list(0, 9)
    return render(request, 'Games/list_test.html', {'game_list': game_list})


def game_info(request, id):
    igdb_api_client = IGDBClient(settings.IGDB_API_KEY, settings.IGDB_API_URL)
    game = igdb_api_client.get_game_by_id(id)
    twitter_api_client = TwitterApi(settings.TWITTER_API_URL,settings.TWITTER_API_KEY, settings.TWITTER_SECRET_API_KEY)
    tweets = twitter_api_client.search_tweets(f'{game.name}')
    return render(request, 'Games/game.html', {'game': game, 
                                               'tweets': tweets})