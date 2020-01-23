import base64
import datetime
from typing import List, TypeVar

import requests


class AuthenticationError(Exception):
    def __init__(self, error_code, error_message):
        self.message = f'Error code {error_code}: {error_message}'


class TwitterApi:
    def __init__(self, api_url: str, api_key: str, api_secret_key: str):
        self._api_url = api_url
        # Encoding for twitter auth
        b64_token = base64.b64encode(
            f'{api_key}:{api_secret_key}'.encode("utf-8"))
        self._token = str(b64_token, 'utf-8')

    @property
    def _authentication_token(self) -> str:
        headers = {'Authorization': f'Basic {self._token}',
                   'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
                   }
        body = {'grant_type': 'client_credentials'}
        data = requests.post(f'{self._api_url}oauth2/token',
                             headers=headers, data=body).json()
        if data.get('errors'):
            first_error = data['errors'][0]
            raise AuthenticationError(
                first_error['code'], first_error['message'])
        else:
            return data['access_token']

    def search_tweets(self, query: str):
        search_headers = {
            'Authorization': f'Bearer {self._authentication_token}'}
        seacrh_params = {'q': query,
                         'lang': 'en'}

        data = requests.get(f'{self._api_url}1.1/search/tweets.json', headers=search_headers,
                            params=seacrh_params).json()

        return [Tweet(tweet_data) for tweet_data in data['statuses']]


class Tweet:
    def __init__(self, data: dict):
        self._data = data
        self.id = data['id']

    @property
    def creation_date(self) -> str:
        date = datetime.datetime.strptime(self._data['created_at'], '%a %b %y %H:%M:%S %z %Y')
        return date.strftime('%d.%m.%Y %H:%M')

    @property
    def text(self) -> str:
        return self._data['text']

    @property
    def user_name(self) -> str:
        return self._data['user']['screen_name']

    @property
    def user_link(self) -> str:
        return f'twitter.com/{self.user_name}'

    @property
    def tweet_link(self) -> str:
        return f'{self.user_link}/status/{self.id}'
