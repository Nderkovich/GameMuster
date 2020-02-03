from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.utils.encoding import force_text
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode
from django.http import HttpResponse, HttpRequest
from django.views.generic import View

from profiles.forms import SignInForm, SignUpForm
from profiles.models import Profile
from profiles.services import send_activation_email, create_confirm_token, check_token
from games.services import get_user_favorite_games


def sign_in(request: HttpRequest) -> HttpResponse:
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


class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'Profiles/sign_up.html', {'form': form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = SignUpForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            if form['password'] == form['confirm_password']:
                user = Profile.objects.create_user(username=form['username'], password=form['password'],
                                                   email=form['email'],
                                                   first_name=form['first_name'], last_name=form['last_name'])
                if user:
                    user.deactivate()
                    send_activation_email(user, create_confirm_token(user),
                                          get_current_site(request))
                    return redirect('user_profile:sign_in')


def profile_view(request: HttpRequest, profile_id: int) -> HttpResponse:
    profile = get_object_or_404(Profile, id=profile_id)
    user_favorites = get_user_favorite_games(profile)
    return render(request, 'Profiles/profile.html', {'profile': profile,
                                                     'user_favorites': user_favorites})


def activation_view(request: HttpRequest, uidb64: str, token: str) -> HttpResponse:
    uid = force_text(urlsafe_base64_decode(uidb64))
    user = get_object_or_404(Profile, id=uid)
    if user is not None and check_token(user, token):
        user.activate()
        return redirect('user_profile:sign_in')
