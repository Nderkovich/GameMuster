from django.conf.urls import include
from django.urls import path
from rest_framework import routers

from api.views import GamesViewSet

router = routers.DefaultRouter()
router.register(r'games', GamesViewSet)


app_name = 'api'


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
