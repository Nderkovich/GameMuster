from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.conf import settings

from profiles_app.models import Profile
from profiles_app.tokens import TokenGenerator
from game_app.igdb_api import IGDBClient


def create_confirm_token(user):
    token_generator = TokenGenerator()
    token = token_generator.make_token(user)
    return token


def send_activation_email(user, token, current_site):
    mail_subject = 'Activate your account.'
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    activation_link = f'{current_site}/activate/uid={uid}/token={token}/'
    message = f'Hello {user.first_name} {user.last_name},\n {activation_link}'
    email = EmailMessage(mail_subject, message, to=[user.email])
    email.send()


def check_token(user, token):
    token_generator = TokenGenerator()
    return token_generator.check_token(user, token)


def get_user_favorite_games(user):
    api_client = IGDBClient(settings.IGDB_API_KEY, settings.IGDB_API_URL)
    ids = []
    for g in user.favorite_games.all():
        ids.append(g.game_id)
    if ids:
        return api_client.get_user_favorites_by_ids(ids)
    else:
        return None
