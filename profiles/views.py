from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate, logout
from django.utils.encoding import force_text
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode
from django.http import HttpResponse, HttpRequest
from django.views.generic import View
from django.contrib import messages
from django.urls import reverse

from profiles.forms import SignInForm, SignUpForm, ProfileInfoForm
from profiles.models import Profile
from profiles.services import create_confirm_token
from profiles.tasks import send_activation_email_task
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
            else:
                messages.warning(request, 'Invalid username or password')
        else:
            messages.warning(request, 'Invalid form data')
    form = SignInForm()
    return render(request, 'Profiles/sign_in.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('games:main_page')


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
                user.deactivate()
                send_activation_email_task.delay(user.id, create_confirm_token(user),
                                                 str(get_current_site(request)))
                return redirect('user_profile:sign_in')
            else:
                messages.warning(request, 'Invalid form data')
                return redirect('user_profile:sign_up')


def profile_view(request: HttpRequest, profile_id: int) -> HttpResponse:
    profile = get_object_or_404(Profile, id=profile_id)
    user_favorites = get_user_favorite_games(profile)
    return render(request, 'Profiles/profile.html', {'profile': profile,
                                                     'user_favorites': user_favorites})


def activation_view(request: HttpRequest, uidb64: str, token: str) -> HttpResponse:
    uid = force_text(urlsafe_base64_decode(uidb64))
    user = get_object_or_404(Profile, id=uid)
    user.activate()
    return redirect('user_profile:sign_in')


class EditProfileView(LoginRequiredMixin, View):
    login_url = '/profile/sign_in/'

    def get(self, request):
        form = ProfileInfoForm()
        return render(request, 'Profiles/edit_profile.html', {'form': form})

    def post(self, request):
        form = ProfileInfoForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            user = request.user
            user.birthday = form['birthday']
            user.first_name = form['first_name']
            user.last_name = form['last_name']
            user.save(update_fields=['birthday', 'first_name', 'last_name'])
            return redirect('user_profile:profile', request.user.id)
        else:
            messages.warning(request, 'Invalid form data')
            return redirect('user_profile:edit_profile', request.user.id)
