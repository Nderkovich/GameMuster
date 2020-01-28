from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfleAdmin(admin.ModelAdmin):
    pass