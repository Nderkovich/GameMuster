from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseNotFound, HttpResponseBadRequest
from django.conf import settings
from django.views import View

from game_app.forms import SearchListForm, SearchNameForm
from game_app.igdb_api import IGDBClient
from game_app.twitter_api import TwitterApi
from game_app.models import Game


def game_list_view(request: HttpRequest, page: int = 1) -> HttpResponse:
    api_client = IGDBClient(settings.IGDB_API_KEY, settings.IGDB_API_URL)
    offset = (page - 1) * settings.GAME_LIST_LIMIT
    list_search_form = SearchListForm()
    name_search_form = SearchNameForm()
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


def game_info(request: HttpRequest, game_id: int) -> HttpResponse:
    igdb_api_client = IGDBClient(settings.IGDB_API_KEY, settings.IGDB_API_URL)
    game = igdb_api_client.get_game_by_id(game_id)
    twitter_api_client = TwitterApi(
        settings.TWITTER_API_URL, settings.TWITTER_API_KEY, settings.TWITTER_SECRET_API_KEY)
    tweets = twitter_api_client.search_tweets(f'"{game.name}"')
    return render(request, 'Games/game.html', {'game': game,
                                               'tweets': tweets})


class SearchView(View):
    api_client = IGDBClient(settings.IGDB_API_KEY, settings.IGDB_API_URL)

    def get(self, request: HttpRequest, page: int = 1) -> HttpResponse:
        list_search_form = SearchListForm()
        name_search_form = SearchNameForm()
        params = self._get_params(request.GET)
        game_list = self._get_game_list(params, page)
        url_params = request.GET.urlencode()
        return render(request, 'Games/list.html', {'game_list': game_list,
                                                   'page': page,
                                                   'list_search_form': list_search_form,
                                                   'name_search_form': name_search_form,
                                                   'params': url_params,
                                                   'url_path': '/search/'})

    def post(self, request: HttpRequest, page: int = 1) -> HttpResponse:
        url_params = request.POST.urlencode()
        return redirect(f'/search/page/1/?{url_params}')

    def _get_params(self, request_dict) -> dict:
        params = {}
        if request_dict.getlist('name'):
            params['name'] = request_dict.getlist('name')[0]
        else:
            params['platforms'] = request_dict.getlist('platforms')
            params['genres'] = request_dict.getlist('genres')
            params['rating_lower_limit'] = request_dict.getlist('rating_lower_limit')[0]
            params['rating_upper_limit'] = request_dict.getlist('rating_upper_limit')[0]
        return params

    def _get_game_list(self, params: dict, page: int) -> list:
        offset = (page - 1) * settings.GAME_LIST_LIMIT
        if params.get('name'):
            return self.api_client.search_games_by_name(params['name'], offset)
        else:
            return self.api_client.search_games_list(params['rating_lower_limit'], params['rating_upper_limit'],
                                                     params['platforms'], params['genres'], offset)


@login_required
def add_to_favorites_view(request: HttpRequest, game_id: HttpResponse):
    try:
        game = Game.objects.get(game_id=game_id)
    except Game.DoesNotExist:
        game = Game(game_id=game_id)
        game.save()
    game.user_profiles.add(request.user)
    game.save()
    return redirect('games:game_info', game_id)


@login_required
def remove_from_favorites_view(request: HttpRequest, game_id: int) -> HttpResponse:
    try:
        game = Game.objects.get(game_id=game_id)
    except Game.DoesNotExist:
        return HttpResponseNotFound()
    if request.user.is_in_favorite(game_id):
        game.user_profiles.remove(request.user)
        game.save()
        return redirect('games:game_info', game_id)
    else:
        return HttpResponseBadRequest()
