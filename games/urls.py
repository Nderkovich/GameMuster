from django.urls import path
from games import views


app_name = 'games'


urlpatterns = [
    path('', views.GameListView.as_view(), name='main_page'),
    path('game/<int:game_id>/', views.game_info, name='game_info'),
    path('search/page/<int:page>/', views.SearchView.as_view(), name='search'),
    path('add_to_favorite/<int:game_id>/', views.add_to_favorites_view, name='add_to_favorite'),
    path('remove_from_favorite/<int:game_id>/', views.remove_from_favorites_view, name='remove_from_favorite')
]
