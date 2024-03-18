import datetime
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mymealmateapp.settings')
django.setup()

from django.contrib.auth import get_user_model
from MyMealMate.models import *


def populate():

    # Create User "test_user" with ShoppingList and Schedule
    UserModel = get_user_model()
    if not UserModel.objects.filter(username='test_user').exists():
        test_user = UserModel.objects.create_user('test_user', password='123', is_superuser=True, is_staff=True)
        profile = UserProfile.objects.create(user=test_user)
        test_user.save()
        profile.save()
    else:
        test_user = UserModel.objects.get(username="test_user")
        profile = UserProfile.objects.get(user=test_user)

    user_shopping_list = ShoppingList.objects.get_or_create(user=test_user)[0]
    user_shopping_list.save()

    user_schedule = Schedule.objects.get_or_create(user=test_user)[0]
    user_schedule.save()

    meals = [{"name": "Spaghetti Bolognese", "url": "https://www.recipetineats.com/spaghetti-bolognese/",
              "instructions": "Cook with love", "image": None},
             {"name": "Pizza", "url": None, "instructions": None, "image": None},
             {"name": "Chili con Carne", "url": None, "instructions": None, "image": None},
             {"name": "Porridge", "url": None, "instructions": None, "image": None},
             ]

    ingredients = [{"name": "Spaghetti", "amount": "300", "unit": "g"},
                   {"name": "Minced Meat", "amount": "500", "unit": "g"},
                   {"name": "Tomato Sauce", "amount": "1", "unit": "kg"},
                   {"name": "Parmesan", "amount": "1", "unit": None},
                   {"name": "Tomato Sauce", "amount": "300", "unit": "ml"},
                   ]

    def add_meal(name, url, image, instructions):
        m = Meal.objects.get_or_create(user=test_user, name=name)[0]
        if url is not None:
            m.url = url
        if image is not None:
            m.image = image
        if instructions is not None:
            m.instructions = instructions
        m.save()
        return m

    def add_ingredient(meal, name, amount, unit):
        i = Ingredient.objects.get_or_create(meal=meal, name=name)[0]
        if amount is not None:
            i.amount = amount
        if unit is not None:
            i.unit = unit
        i.save()
        return i

    # add Meals
    for m in meals:
        add_meal(m["name"], m["image"], m["url"], m["instructions"])

    # add Ingredients
    for i in ingredients[:-1]:
        add_ingredient(Meal.objects.get(name="Spaghetti Bolognese"), i["name"], i["amount"], i["unit"])
    add_ingredient(Meal.objects.get(name="Pizza"), ingredients[-1]["name"], ingredients[-1]["amount"], ingredients[-1]["unit"])

    # add ingredients to shopping list
    for i in Ingredient.objects.all():
        user_shopping_list.add_ingredient(i)

    # schedule all Meals for today
    new_day = Day(schedule=user_schedule, date=datetime.date.today())
    new_day.save()
    for m in Meal.objects.all():
        user_schedule.scheduleMeal(new_day, m)
    user_schedule.save()


if __name__ == "__main__":
    print("Starting MyMealMate population script...")
    populate()
