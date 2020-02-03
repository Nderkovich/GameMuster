from django.contrib import admin
from game_app.models import Game


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    pass
