from django.contrib import admin
from game_app.models import Game, Screenshot, Keyword, Genre, Platform


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    pass


@admin.register(Screenshot)
class ScreenshotAdmin(admin.ModelAdmin):
    pass


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    pass


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    pass
