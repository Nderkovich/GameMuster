from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.conf import settings
from django.views import View
from django.core.paginator import Paginator

from game_app.forms import SearchListForm, SearchNameForm
from game_app.igdb_api import IGDBClient
from game_app.twitter_api import TwitterApi
from game_app.models import Game


def game_list_view(request: HttpRequest, page: int = 1) -> HttpResponse:
    if request.method == 'POST':
        url_params = request.POST.urlencode()
        return redirect(f'/search/page/1/?{url_params}')
    list_search_form = SearchListForm()
    name_search_form = SearchNameForm()
    games = Game.objects.all()
    paginator = Paginator(games, settings.GAME_LIST_LIMIT)
    game_list = paginator.get_page(page).object_list
    return render(request, 'Games/list.html', {'game_list': game_list,
                                               'page': page,
                                               'list_search_form': list_search_form,
                                               'name_search_form': name_search_form,
                                               'params': "",
                                               'url_path': "/"})


def game_info(request: HttpRequest, game_id: int) -> HttpResponse:
    game = get_object_or_404(Game, game_id=game_id)
    twitter_api_client = TwitterApi(
        settings.TWITTER_API_URL, settings.TWITTER_API_KEY, settings.TWITTER_SECRET_API_KEY)
    tweets = twitter_api_client.search_tweets(f'"{game.game_name}"')
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
