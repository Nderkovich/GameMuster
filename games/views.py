from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, HttpResponseBadRequest
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.conf import settings
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect

from games.forms import SearchListForm, SearchNameForm
from games.igdb_api import IGDBClient
from games.twitter_api import TwitterApi
from games.models import Game


class GameInfoView(DetailView):
    model = Game
    template_name = "Games/game.html"

    def get_object(self, **kwargs):
        return get_object_or_404(Game, game_id=self.kwargs['game_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        twitter_api_client = TwitterApi(
            settings.TWITTER_API_URL, settings.TWITTER_API_KEY, settings.TWITTER_SECRET_API_KEY)
        context['tweets'] = twitter_api_client.search_tweets(f'"{self.object.game_name}"')
        return context


class GameListView(ListView):
    api_client = IGDBClient(settings.IGDB_API_KEY, settings.IGDB_API_URL)
    model = Game
    paginate_by = settings.GAME_LIST_LIMIT
    template_name = "Games/list.html"
    params = None

    def get(self, *args, **kwargs):
        if self.request.GET.get('csrfmiddlewaretoken'):
            params = self.request.GET.copy()
            return redirect(f'/?{params.urlencode()}')
        else:
            return super(GameListView, self).get(*args, **kwargs)

    def get_queryset(self, **kwargs):
        params = self._get_params(self.request.GET)
        return self._get_game_list(params)

    def get_context_data(self, *, object_list=None, **kwargs) -> HttpResponse:
        context = super().get_context_data(**kwargs)
        list_search_form = SearchListForm(self.request.GET)
        name_search_form = SearchNameForm(self.request.GET)
        context['list_search_form'] = list_search_form
        context['name_search_form'] = name_search_form
        context['params'] = self.request.GET.urlencode()
        return context

    def _get_params(self, request_dict) -> dict:
        MINIMUN_RATING = 0
        MAXIMUM_RATING = 100
        params = {}
        if request_dict.getlist('name'):
            params['name'] = request_dict.getlist('name')[0]
        else:
            params['platforms'] = request_dict.getlist('platforms')
            params['genres'] = request_dict.getlist('genres')
            params['rating_lower_limit'] = request_dict.getlist('rating_lower_limit', default=[MINIMUN_RATING])[0]
            params['rating_upper_limit'] = request_dict.getlist('rating_upper_limit', default=[MAXIMUM_RATING])[0]
        return params

    def _get_game_list(self, params: dict) -> Paginator:
        if params.get('name'):
            games = Game.objects.filter(game_name__icontains=params['name']).all()
            return games
        else:
            games = Game.objects.filter(user_rating__gte=int(params['rating_lower_limit']),
                                        user_rating__lte=int(params['rating_upper_limit'])).all()
            if params['platforms']:
                games = games.filter(platforms__platform_abbreviation__in=params['platforms']).all()
            if params['genres']:
                games = games.filter(genres__genre_name__in=params['genres']).all()
            games = games.distinct()
            return games


@login_required
def add_to_favorites_view(request: HttpRequest, game_id: HttpResponse):
    try:
        game = Game.objects.get(game_id=game_id)
    except Game.DoesNotExist:
        game = Game(game_id=game_id)
        game.save()
    game.user_profiles.add(request.user)
    game.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def remove_from_favorites_view(request: HttpRequest, game_id: int) -> HttpResponse:
    try:
        game = Game.objects.get(game_id=game_id)
    except Game.DoesNotExist:
        return HttpResponseNotFound()
    if request.user.is_in_favorite(game_id):
        game.user_profiles.remove(request.user)
        game.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseBadRequest()
