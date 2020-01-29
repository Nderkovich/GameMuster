from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.conf import settings
from django.views import View
from django.contrib.auth import login, authenticate
from django.utils.encoding import force_text
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode


from game_app.forms import SearchListForm, SearchNameForm, SignInForm, SignUpForm
from game_app.models import Profile
from game_app.igdb_api import IGDBClient
from game_app.twitter_api import TwitterApi
from game_app.services import send_activation_email, create_confirm_token, check_token


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

    def get(self, request, page=1):
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

    def post(self, request, page=1):
        url_params = request.POST.urlencode()
        return redirect(f'/search/page/1/?{url_params}')

    def _get_params(self, request_dict):
        params = {}
        if request_dict.getlist('name'):
            params['name'] = request_dict.getlist('name')[0]
        else:
            params['platforms'] = request_dict.getlist('platforms')
            params['genres'] = request_dict.getlist('genres')
            params['rating_lower_limit'] = request_dict.getlist('rating_lower_limit')[0]
            params['rating_upper_limit'] = request_dict.getlist('rating_upper_limit')[0]
        return params

    def _get_game_list(self, params, page):
        offset = (page - 1) * settings.GAME_LIST_LIMIT
        if params.get('name'):
            return self.api_client.search_games_by_name(params['name'], offset)
        else:
            return self.api_client.search_games_list(params['rating_lower_limit'], params['rating_upper_limit'],
                                                     params['platforms'], params['genres'], offset)


def sign_in(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            user = authenticate(
                request, username=form['username'], password=form['password'])
            if user is not None:
                login(request, user)
                return redirect('games:main_page')
    form = SignInForm()
    return render(request, 'Games/sign_in.html', {'form': form})


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            if form['password'] == form['confirm_password']:
                user = Profile.objects.create_user(username=form['username'], password=form['password'], email=form['email'],
                                                   first_name=form['first_name'], last_name=form['last_name'])
                if user:
                    user.is_active = False
                    user.save()
                    send_activation_email(user, create_confirm_token(user),
                                          get_current_site(request))
                    return redirect('games:sign_in')
    form = SignUpForm()
    return render(request, 'Games/sign_up.html', {'form': form})


def profile_view(request, id):
    profile = get_object_or_404(Profile, id=id)
    return render(request, 'Games/profile.html', {'profile': profile})


def activation_view(request, uidb64, token):
    uid = force_text(urlsafe_base64_decode(uidb64))
    user = get_object_or_404(Profile, id=uid)
    if user is not None and check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('games:sign_in')
