from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from MyMealMate.models import UserProfile

# Create your tests here.
class LoginTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create_user('testUser', 'test@test.com', 'testPassword')
        UserProfile.objects.create(user=self.test_user)

    def test_login_success(self):
        response = self.client.post(reverse('MyMealMate:home'), {'username': 'testUser', 'password': 'testPassword'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('MyMealMate:user_hub'))

    def test_login_fail(self):
        response = self.client.post(reverse('MyMealMate:home'), {'username': 'wronguser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
