from django.conf.urls import include
from django.urls import path

from api.views import GamesView, GameInfoView


app_name = 'api'

urlpatterns = [
    path('', GamesView.as_view()),
    path('<int:game_id>/', GameInfoView.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
