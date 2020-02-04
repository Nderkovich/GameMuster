from django.contrib import admin
from profiles.models import Profile


@admin.register(Profile)
class ProfleAdmin(admin.ModelAdmin):
    pass
