from django.test import TestCase, Client
from django.contrib.auth.models import User

# Create your tests here.
class LoginTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
    
    def test_login_success(self):
        response = self.client.post("{% url 'MyMealMate: home}' %}", {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "{% url 'MyMealMate: user_hub}' %}")

    def test_login_fail(self):
        response = self.client.post("{% url 'MyMealMate: home}' %}", {'username': 'wronguser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.url, "{% url 'MyMealMate: home}' %}")
