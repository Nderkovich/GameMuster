from django.urls import path
from . import views


app_name = 'games'


urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('game/<int:id>/', views.game_info, name='game_info')
]
