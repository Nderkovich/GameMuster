from rest_framework import viewsets
from django.http import Http404
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import GameSerializer
from games.models import Game


class GamesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def get_object(self, *args, **kwargs,):
        game = get_object_or_404(Game, game_id=self.kwargs['pk'])
        serializer = GameSerializer(game)
        return serializer.data
