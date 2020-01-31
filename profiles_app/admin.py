from django.contrib import admin
from profiles_app.models import Profile


@admin.register(Profile)
class ProfleAdmin(admin.ModelAdmin):
    pass
