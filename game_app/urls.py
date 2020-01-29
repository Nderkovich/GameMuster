from django.urls import path
from . import views


app_name = 'games'


urlpatterns = [
    path('', views.game_list, name='main_page'),
    path('page/<int:page>/', views.game_list, name='gamelist_page'),
    path('game/<int:id>/', views.game_info, name='game_info'),
    path('search/page/<int:page>/', views.SearchView.as_view(), name='search'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('profile/<int:id>', views.profile, name='profile'),
    path('activate/uid=<str:uidb64>/token=<str:token>/', views.activate, name='activation')
]
