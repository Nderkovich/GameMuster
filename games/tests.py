from django.test import Client, TestCase, RequestFactory
from django.urls import reverse
from games.models import Game
from games.views import remove_from_favorites_view
from profiles.models import Profile


class MyTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = Profile.objects.create(
            username="user_test",
            password="12345Da",
            email="email@adasdasfsdf.ru",
            first_name="Name",
            last_name="Name"
        )

    def test_game_not_exist(self):
        response = self.client.get(reverse('games:game_info', args=(1, )))
        self.assertEqual(response.status_code, 404)

    def test_game_exist(self):
        game = Game.objects.create(game_id=1)
        response = self.client.get(reverse('games:game_info', args=(game.game_id, )))
        self.assertEqual(response.status_code, 200)

    def test_search_game(self):
        response = self.client.get('/', {'name': 'game_name'})
        self.assertEqual(response.status_code, 200)

    def test_game_not_favorite(self):
        game = Game.objects.create(game_id=1)
        request = self.factory.get(reverse('games:remove_from_favorite', args=(game.game_id, )))
        request.user = self.user
        response = remove_from_favorites_view(request, 1)
        self.assertEqual(response.status_code, 400)
