from django.test import TestCase, Client
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse

from MyMealMate.models import *
from MyMealMate.forms import *
from MyMealMate.views import *

# Anna's tests

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

# Katie's tests
class TestLoginAndSignup(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_username = 'testUser'
        self.test_password = 'testPassword123'
        self.test_user = User.objects.create_user(self.test_username, "test@test.com", self.test_password)
        UserProfile.objects.create(user = self.test_user)

    def test_login_success(self):
        # correct username and password
        response = self.client.post(reverse('MyMealMate:home'), {'username': self.test_username, 'password': self.test_password})
        self.assertEqual(response.status_code, 302)

    def test_login_wrong_password(self):
        # incorrect password
        response = self.client.post(reverse('MyMealMate:home'), {'username': self.test_username, 'password': 'incorrectPassword'})
        self.assertEqual(response.status_code, 200)

<<<<<<< HEAD
    def test_login_wrong_username(self):
        # incorrect username
        response = self.client.post(reverse('MyMealMate:home'), {'username': 'wrongUsername', 'password': self.test_password})
        self.assertEqual(response.status_code, 200)

    def test_signup_success(self):
        # create new user
        response = self.client.post(reverse('MyMealMate:signup'), {'username': 'newTestUser', 'first_name': 'User', 'email': 'newUser@test.com', 'password': 'testPassword123'})
        self.assertEqual(response.status_code, 302)

    def test_signup_taken_username(self):
        # username already taken
        response = self.client.post(reverse('MyMealMate:signup'), {'username': self.test_username, 'first_name': 'testUser', 'email': 'newUSer2@new.com', 'password': 'newTestPassword123'})
        self.assertEqual(response.status_code, 200)

    def test_signup_no_details(self):
        # no details entered
        response = self.client.post(reverse('MyMealMate:signup'), {})
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        # logout
        self.client.login(username=self.test_username, password=self.test_password)
        response = self.client.post(reverse('MyMealMate:logout'), {})
        self.assertEqual(response.status_code, 302)



class TestProfile(TestCase):
    def test_profile_view(self):
        # test profile view
        self.client = Client()
        self.test_username = 'testUser'
        self.test_password = 'testPassword123'
        self.test_user = User.objects.create_user(self.test_username, "test@test.com", self.test_password)
        UserProfile.objects.create(user = self.test_user)
        self.client.login(username=self.test_username, password=self.test_password)

        response = self.client.get(reverse('MyMealMate:profile')) 

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.test_username)
        self.assertContains(response, "default_profile.jpg")
        self.client.logout()
        response = self.client.get(reverse('MyMealMate:profile'))
        self.assertEqual(response.status_code, 302)

    def test_edit_view(self):
        self.client = Client()
        self.test_username = 'testUser'
        self.test_password = 'testPassword123'
        self.test_user = User.objects.create_user(self.test_username, "test@test.com", self.test_password)
        UserProfile.objects.create(user = self.test_user)
        self.client.login(username=self.test_username, password=self.test_password)
        response = self.client.get(reverse('MyMealMate:edit_profile'))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.test_username)
        response = self.client.post(reverse('MyMealMate:edit_profile'), {'username': 'updatedUsername', 'first_name': 'updatedName', 'email': 'updatedTest@test.com'})
        self.assertEqual(response.status_code, 302)

        updated_user = User.objects.get(username='updatedUsername')
        self.assertEqual(updated_user.first_name, 'updatedName')
        self.assertEqual(updated_user.email, 'updatedTest@test.com')

        response = self.client.get(reverse('MyMealMate:profile')) 
        self.assertContains(response, "default_profile.jpg")

        self.client.logout()
        response = self.client.get(reverse('MyMealMate:edit_profile'))
        self.assertEqual(response.status_code, 302)

=======
class MealViewsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_new_meal(self):
        request = self.factory.post(reverse('MyMealMate:new_meal'), {'name': 'Test Meal'})
        request.user = self.user
        response = new_meal(request)
        self.assertEqual(response.status_code, 302)  # Check if redirect occurs
        self.assertTrue(Meal.objects.filter(user=self.user, name='Test Meal').exists())  # Check if meal was added

    def test_delete_meal(self):
        request = self.factory.post(reverse('MyMealMate:new_meal'), {'name': 'Test Meal'})
        request.user = self.user
        response = delete_meal(request)
        self.assertEqual(response.status_code, 302)  # Check if redirect occurs
        self.assertFalse(Meal.objects.filter(user=self.user, name='Test Meal').exists())  # Check if meal was added

    def test_add_ingredient(self):
        user, user_profile = create_user_object()
        request = self.factory.post('/add_ingredient/', {'name': 'Milk', 'amount': '2', 'unit': 'liters'})
        request.user = user
        response = add_ingredient(request)
        self.assertEqual(response.status_code, 200)
>>>>>>> main
