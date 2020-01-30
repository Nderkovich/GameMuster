from django.urls import path
from . import views


app_name = 'games'


urlpatterns = [
    path('', views.game_list_view, name='main_page'),
    path('page/<int:page>/', views.game_list_view, name='game_list_page'),
    path('game/<int:game_id>/', views.game_info, name='game_info'),
    path('search/page/<int:page>/', views.SearchView.as_view(), name='search')
]
