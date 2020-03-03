from games.models import Game, Keyword, Screenshot, Genre, Platform
from rest_framework import serializers


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = (
            'keyword_id',
            'keyword_name'
        )


class ScreenshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screenshot
        fields = (
            'screen_thumb_url',
            'screen_big_url'
        )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            'genre_id',
            'genre_name'
        )


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = (
            'platform_id',
            'platform_name',
            'platform_abbreviation'
        )


class GameSerializer(serializers.ModelSerializer):
    keywords = KeywordSerializer(read_only=True, many=True)
    screenshots = ScreenshotSerializer(read_only=True, many=True)
    genres = GenreSerializer(read_only=True, many=True)
    platforms = PlatformSerializer(read_only=True, many=True)

    class Meta:
        model = Game
        fields = ('game_id', 'game_name', 'cover_url', 'user_rating', 'user_rating_count', 'critic_rating',
                  'critic_rating_count', 'game_description', 'game_release_date', 'user_profiles', 'keywords',
                  'screenshots', 'genres', 'platforms')
