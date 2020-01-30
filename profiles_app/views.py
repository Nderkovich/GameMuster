from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.utils.encoding import force_text
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest, HttpResponseNotFound, HttpResponseBadRequest

from profiles_app.forms import SignInForm, SignUpForm
from profiles_app.models import Profile, Game
from profiles_app.services import send_activation_email, create_confirm_token, check_token, get_user_favorite_games


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
    return render(request, 'Profiles/sign_in.html', {'form': form})


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
                    return redirect('user_profile:sign_in')
    form = SignUpForm()
    return render(request, 'Profiles/sign_up.html', {'form': form})


def profile_view(request, id: int):
    profile = get_object_or_404(Profile, id=id)
    user_favorites = get_user_favorite_games(profile)
    return render(request, 'Profiles/profile.html', {'profile': profile,
                                                  'user_favorites': user_favorites})


def activation_view(request, uidb64, token):
    uid = force_text(urlsafe_base64_decode(uidb64))
    user = get_object_or_404(Profile, id=uid)
    if user is not None and check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('user_profile:sign_in')


@login_required
def add_to_favorites_view(request, game_id):
    game = Game.objects.filter(game_id=game_id).first()
    if not game:
        game = Game(game_id=game_id)
        game.save()
    game.user_profiles.add(request.user)
    game.save()
    return redirect('games:game_info', game_id)


@login_required
def remove_from_favorites_view(request, game_id):
    game = Game.objects.filter(game_id=game_id).first()
    if game:
        if request.user.is_in_favorite(game_id):
            game.user_profiles.remove(request.user)
            game.save()
            return redirect('games:game_info', game_id)
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseNotFound()
