import base64
import datetime
from typing import List

import requests


class AuthenticationError(Exception):
    def __init__(self, error_code, error_message):
        self.message = f'Error code {error_code}: {error_message}'


class TwitterError(Exception):
    def __init__(self, error_code):
        self.message = f'Tweet erro {error_code}'


class Tweet:
    def __init__(self, tweet_id, text, user_name, date):
        self.tweet_id = tweet_id
        self.text = text
        self.user_name = user_name
        self.creation_date = date

    @property
    def creation_date(self) -> str:
        return self._creation_date

    @creation_date.setter
    def creation_date(self, tweet_date):
        date = datetime.datetime.strptime(
            tweet_date, '%a %b %y %H:%M:%S %z %Y')
        self._creation_date = date.strftime('%d.%m.%Y %H:%M')

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, tweet_text):
        self._text = tweet_text

    @property
    def user_name(self) -> str:
        return self._user_name

    @user_name.setter
    def user_name(self, twitter_user_name):
        self._user_name = twitter_user_name

    @property
    def user_link(self) -> str:
        return f'twitter.com/{self.user_name}'

    @property
    def tweet_link(self) -> str:
        return f'{self.user_link}/status/{self.tweet_id}'


class TwitterApi:
    def __init__(self, api_url: str, api_key: str, api_secret_key: str):
        self._api_url = api_url
        # Encoding for twitter auth
        b64_token = base64.b64encode(
            f'{api_key}:{api_secret_key}'.encode("utf-8"))
        encoded_token = str(b64_token, 'utf-8')
        self._bearer_token = self._get_authentication_token(encoded_token)

    def _get_authentication_token(self, encoded_token) -> str:
        headers = {'Authorization': f'Basic {encoded_token}',
                   'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
                   }
        body = {'grant_type': 'client_credentials'}
        response = requests.post(f'{self._api_url}oauth2/token',
                                 headers=headers, data=body)
        print(f'{self._api_url}oauth2/token')
        print(response)
        print(headers)
        print(body)
        if not response.ok:
            raise TwitterError(response.status_code)
        else:
            data = response.json()
            return data['access_token']

    def search_tweets(self, query: str) -> List[Tweet]:
        search_headers = {
            'Authorization': f'Bearer {self._bearer_token}'}
        seacrh_params = {'q': query,
                         'lang': 'en'}
        response = requests.get(f'{self._api_url}1.1/search/tweets.json', headers=search_headers,
                                params=seacrh_params)
        if not response.ok:
            raise TwitterError(response.status_code)
        data = response.json()
        return [Tweet(tweet_data['id'], tweet_data['text'], tweet_data['user']['screen_name'],
                      tweet_data['created_at']) for tweet_data in data['statuses']]
