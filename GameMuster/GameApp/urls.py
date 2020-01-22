from django.urls import path
from . import views


app_name='Game'


urlpatterns = [
    path('', views.list_test, name='mainp'),
    path('info/', views.detailpage, name='info'),
    path('game/<int:id>/', views.game_info, name='game')
]