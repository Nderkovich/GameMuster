from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.conf import settings
from .forms import SearchListForm, SearchNameForm

from .igdb_api import IGDBClient
from .twitter_api import TwitterApi


def game_list(request: HttpRequest, page: int = 1) -> HttpResponse:
    api_client = IGDBClient(settings.IGDB_API_KEY, settings.IGDB_API_URL)
    offset = (page - 1) * settings.GAME_LIST_LIMIT
    list_search_form = SearchListForm()
    name_search_form = SearchNameForm()
    url_params = ""
    if request.method == 'POST':
        url_params = request.POST.urlencode()
        return redirect(f'/search/page/1/?{url_params}')
    game_list = api_client.get_game_list(offset)
    return render(request, 'Games/list.html', {'game_list': game_list,
                                               'page': page,
                                               'list_search_form': list_search_form,
                                               'name_search_form': name_search_form,
                                               'params': "",
                                               'url_path': "/"})


def game_info(request: HttpRequest, id: int) -> HttpResponse:
    igdb_api_client = IGDBClient(settings.IGDB_API_KEY, settings.IGDB_API_URL)
    game = igdb_api_client.get_game_by_id(id)
    twitter_api_client = TwitterApi(
        settings.TWITTER_API_URL, settings.TWITTER_API_KEY, settings.TWITTER_SECRET_API_KEY)
    tweets = twitter_api_client.search_tweets(f'"{game.name}"')
    return render(request, 'Games/game.html', {'game': game,
                                               'tweets': tweets})


def search(request: HttpRequest, page=1) -> HttpResponse:
    params = {}
    api_client = IGDBClient(settings.IGDB_API_KEY, settings.IGDB_API_URL)
    offset = (page - 1) * settings.GAME_LIST_LIMIT
    list_search_form = SearchListForm()
    name_search_form = SearchNameForm()
    if request.method == 'POST':
        url_params = request.POST.urlencode()
        return redirect(f'/search/page/1/?{url_params}')
    if request.GET.getlist('name'):
        game_list = api_client.search_games_by_name(request.GET.getlist('name')[0], offset)
    else:
        params['platforms'] = request.GET.getlist('platforms')
        params['genres'] = request.GET.getlist('genres')
        params['rating_lower_limit'] = request.GET.getlist('rating_lower_limit')[0]
        params['rating_upper_limit'] = request.GET.getlist('rating_upper_limit')[0]
        game_list = api_client.search_games_list(params['rating_lower_limit'],
                                                 params['rating_upper_limit'], params['platforms'], params['genres'], offset)
    url_params = request.GET.urlencode()
    return render(request, 'Games/list.html', {'game_list': game_list,
                                               'page': page,
                                               'list_search_form': list_search_form,
                                               'name_search_form': name_search_form,
                                               'params': url_params,
                                               'url_path': '/search/'})
