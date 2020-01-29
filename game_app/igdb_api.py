from datetime import datetime
from django.conf import settings
from typing import List, Dict, Optional

import requests


class ApiException(Exception):
    def __init__(self, error_code):
        self.message = f'Error code {error_code}'


class Game:
    def __init__(self, id, data):
        self.id = id
        self._data = data

    @property
    def name(self) -> str:
        return self._data['name']

    @property
    def critics_rating(self) -> Dict[str, int]:
        critics_rate = {'rating': int((self._data.get('aggregated_rating', 0))),
                        'count': self._data.get('aggregated_rating_count', 0)}
        return critics_rate

    @property
    def user_rating(self) -> Dict[str, int]:
        users_rate = {'rating': int((self._data.get('rating', 0))),
                      'count': self._data.get('rating_count', 0)}
        return users_rate

    @property
    def release_date(self) -> Optional[datetime]:
        if self._data.get('first_release_date'):
            return datetime.utcfromtimestamp(self._data['first_release_date']).strftime('%d %B %Y')
        else:
            return None

    @property
    def genres(self) -> List[str]:
        genres_list = []
        if self._data.get('genres'):
            for genre in self._data['genres']:
                genres_list.append(genre['name'])
        return genres_list

    @property
    def platforms(self) -> List[str]:
        platforms_list = []
        if self._data.get('platforms'):
            for platform in self._data['platforms']:
                if platform.get('abbreviation'):
                    platforms_list.append(platform['abbreviation'])
                else:
                    platforms_list.append(platform['name'])
        return platforms_list

    @property
    def summary(self) -> str:
        return self._data.get('summary')

    @property
    def thubm_screenshots(self) -> List[str]:
        screenshots = []
        if self._data.get('screenshots'):
            for screenshot in self._data['screenshots']:
                screenshots.append(screenshot['url'])
        return screenshots

    @property
    def big_screenshots(self) -> List[str]:
        thumb_screenshots = self.thubm_screenshots
        big_screenshots = []
        for screen in thumb_screenshots:
            big_screenshots.append(screen.replace(
                't_thumb', 't_screenshot_big'))
        return big_screenshots

    @property
    def keywords(self) -> List[str]:
        keywords = []
        if self._data.get('keywords'):
            for keyword in self._data['keywords']:
                keywords.append(keyword['name'])
        return keywords

    @property
    def cover(self) -> str:
        if self._data.get('cover'):
            return self._data['cover']['url'].replace('thumb', 'cover_big')
        else:
            return None


class IGDBClient:

    def __init__(self, user_key: str, api_url: str):
        self.headers = {'user-key': user_key}
        self.api_url = api_url

    def _get_game_data_by_id(self, id: int, needed_info: List[str]) -> dict:
        url = self.api_url + 'games'
        body = f"fields {str(needed_info)[1:-1]};  where id = {id};"
        response = requests.post(url, headers=self.headers, data=body)
        if not response.ok:
            raise ApiException(response.status_code)
        return response.json()

    def _get_games_data(self, offset: int, limit: int) -> dict:
        url = self.api_url + 'games'
        body = f'fields name, genres.name, cover.url, first_release_date, keywords.name;limit {limit};offset {offset};'
        response = requests.post(url, headers=self.headers, data=body)
        if not response.ok:
            raise ApiException(response.status_code)
        return response.json()

    def _build_search_query(self, lower_limit: int, upper_limit: int, platforms: Optional[List[str]] = None, genres: Optional[List[str]] = None) -> str:
        query = f'where rating>{lower_limit} & rating<{upper_limit} '
        if platforms:
            str_platforms = (str(platforms)[1:-1]).replace("'", '"')
            query += f'& platforms.abbreviation=({str_platforms}) '
        if genres:
            str_genres = (str(genres)[1:-1]).replace("'", '"')
            query += f'& genres.name=({str_genres})'
        query += ';'
        return query

    def _search_games_params(self, lower_limit: int, upper_limit: int, platforms: Optional[List[str]] = None, genres: Optional[List[str]] = None,  offset=0, limit=9) -> dict:
        url = self.api_url + 'games'
        query = self._build_search_query(
            lower_limit, upper_limit, platforms, genres)
        body = f'fields name, genres.name, cover.url, first_release_date, keywords.name;limit {limit};offset {offset};{query}'
        response = requests.post(url, headers=self.headers, data=body)
        if not response.ok:
            raise ApiException(response.status_code)
        return response.json()

    def _search_games_name(self, name, offset=0, limit=9) -> dict:
        url = self.api_url + 'games'
        body = f'search "{name}";fields name, genres.name, cover.url, first_release_date, keywords.name;limit {limit};offset {offset};'
        response = requests.post(url, headers=self.headers, data=body)
        if not response.ok:
            raise ApiException(response.status_code)
        return response.json()

    def get_game_by_id(self, id: int) -> Game:
        data = self._get_game_data_by_id(id, ['aggregated_rating', 'aggregated_rating_count', 'first_release_date',
                                              'genres.name', 'keywords.name', 'name', 'platforms.name',
                                              'platforms.abbreviation', 'rating', 'rating_count', 'cover.url', 'summary',
                                              'screenshots.url'])[0]
        return Game(id, data)

    def get_game_list(self, offset=0, limit=9) -> List[Game]:
        data = self._get_games_data(offset, limit)
        return [Game(game_data['id'], game_data) for game_data in data]

    def search_games_list(self, lower_limit: int, upper_limit: int, platforms: Optional[List[str]] = None, genres: Optional[List[str]] = None,  offset: int = 0, limit: int = 9) -> List[Game]:
        data = self._search_games_params(
            lower_limit, upper_limit, platforms, genres, offset, limit)
        return [Game(game_data['id'], game_data) for game_data in data]

    def search_games_by_name(self, name: str, offset: int = 0, limit: int = 9) -> List[Game]:
        data = self._search_games_name(name, offset, limit)
        return [Game(game_data['id'], game_data) for game_data in data]
