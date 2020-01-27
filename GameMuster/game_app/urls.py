from django.urls import path
from . import views


app_name = 'games'


urlpatterns = [
    path('', views.game_list, name='main_page'),
    path('page/<int:page>/', views.game_list, name='gamelist_page'),
    path('game/<int:id>/', views.game_info, name='game_info')
]
