from django.test import TestCase, Client
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse

from MyMealMate.models import *
from MyMealMate.forms import *
from MyMealMate.views import *

def create_user_object():
    """
    Helper function to create a User object.
    """
    UserModel = get_user_model()
    if not UserModel.objects.filter(username='test_user').exists():
        test_user = UserModel.objects.create_user('test_user', password='123', is_superuser=True, is_staff=True)
        user_profile = UserProfile.objects.create(user=test_user)
        test_user.save()
        user_profile.save()
    else:
        test_user = UserModel.objects.get(username="test_user")
        user_profile = UserProfile.objects.get(user=test_user)

    return test_user, user_profile


class TestShoppingListFunctionality(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_add_new_ingredient(self):
        user, user_profile = create_user_object()
        shopping_list = ShoppingList.objects.get_or_create(user=user)[0]

        shopping_list.add_item("Flour", 100, "g")
        self.assertTrue(ShoppingListItem.objects.filter(shoppingList=shopping_list, name="Flour").exists())

    def test_add_amount_to_ingredient(self):
        user, user_profile = create_user_object()
        shopping_list = ShoppingList.objects.get_or_create(user=user)[0]

        shopping_list.add_item("Flour", 100, "g")
        old_amount = ShoppingListItem.objects.filter(shoppingList=shopping_list, name="Flour")[0].amount
        shopping_list.add_item("Flour", 100, "g")
        self.assertEqual(ShoppingListItem.objects.filter(shoppingList=shopping_list, name="Flour")[0].amount, old_amount+100)

    def test_add_shopping_list_item_post(self):
        user, user_profile = create_user_object()
        request = self.factory.post('/add_item/', {'name': 'Milk', 'amount': '2', 'unit': 'liters'})
        request.user = user
        response = add_shopping_list_item(request)
        self.assertEqual(response.status_code, 200)

    def test_add_shopping_list_item_negative_amount(self):
        user, user_profile = create_user_object()
        request = self.factory.post('/add_item/', {'name': 'Bread', 'amount': '-1', 'unit': 'loaf'})
        request.user = user
        response = add_shopping_list_item(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.content.decode('utf-8'))

    def test_add_shopping_list_item_get(self):
        user, user_profile = create_user_object()
        request = self.factory.get('/add_item/')
        request.user = user
        response = add_shopping_list_item(request)
        self.assertEqual(response.status_code, 405)
        self.assertIn('error', response.content.decode('utf-8'))

    def test_delete_shopping_list_item(self):
        user, user_profile = create_user_object()
        shopping_list = ShoppingList.objects.get_or_create(user=user)[0]

        item = shopping_list.add_item("Flour", 100, "g")

        response = self.client.post(reverse('MyMealMate:delete_item'), {'item_id': item.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Item deleted successfully'})

    def test_delete_shopping_list_item_error(self):
        response = self.client.get(reverse('MyMealMate:delete_item'))
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json(), {'error': 'Method not allowed'})


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

class MealViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.meal = Meal.objects.create(name='Test Meal', user=self.user)