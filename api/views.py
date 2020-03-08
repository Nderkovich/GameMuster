from rest_framework.generics import ListAPIView, RetrieveAPIView

from api.serializers import GameSerializer
from games.models import Game


class GamesView(ListAPIView):
    serializer_class = GameSerializer
    queryset = Game.objects.all()


class GameInfoView(RetrieveAPIView):
    lookup_field = "game_id"
    serializer_class = GameSerializer
    queryset = Game.objects.all()

