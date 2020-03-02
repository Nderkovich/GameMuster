from rest_framework import viewsets

from api.serializers import GameSerializer
from games.models import Game


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer