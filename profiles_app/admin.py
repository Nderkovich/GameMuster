from django.contrib import admin
from profiles_app.models import Profile, Game


@admin.register(Profile)
class ProfleAdmin(admin.ModelAdmin):
    pass

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    pass
