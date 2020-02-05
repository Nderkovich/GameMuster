from django.test import TestCase, Client
from profiles.models import Profile

# Create your tests here.
class ProfilesTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login(self):
        usr = Profile.objects.create(
            username="user1",
            first_name="Name",
            last_name='Name',
            email="email@gmail.com",
            password='12345Da'
        )
        response = self.client.post('/profile/sign_in/', {'username': "user1", "password": '12345Da'})
        self.assertEqual(response.status_code, 200)

    def test_registration(self):
        response = self.client.post('/profile/sign_up/', {'username': "user1",
                                                          'password': "12345Da",
                                                          'confirm_password': "12345Da",
                                                          'email': "email@adasdasfsdf.ru",
                                                          'first_name': "Name",
                                                          'last_name': "Name"})
        self.assertEqual(response.status_code, 302)

    def test_profile_not_exist(self):
        response = self.client.get('/profile/profile/2/')
        self.assertEqual(response.status_code, 404)
