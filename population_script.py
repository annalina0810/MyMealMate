import datetime
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mymealmateapp.settings')
django.setup()

from django.core.files import File
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
              "instructions": "Cook with love", "image": "spaghetti-bolognese.jpg"},
             {"name": "Pizza", "url": None, "instructions": None, "image": "pizza.jpg"},
             {"name": "Chili con Carne", "url": None, "instructions": None, "image": "chili-con-carne.jpg"},
             {"name": "Porridge", "url": None, "instructions": None, "image": "porridge.jpg"},
             ]

    spaghetti_ingredients = [{"name": "Spaghetti", "amount": "300", "unit": "g"},
                   {"name": "Minced Meat", "amount": "500", "unit": "g"},
                   {"name": "Tomato Sauce", "amount": "1", "unit": "kg"},
                   {"name": "Parmesan", "amount": "1", "unit": None},
                   {"name": "Onions", "amount": "2", "unit": None},
                   {"name": "Garclic cloves", "amount": "3", "unit": None},
                   ]
    chili_ingredients = [{"name": "Minced Meat", "amount": "500", "unit": "g"},
                   {"name": "Tomato Sauce", "amount": "300", "unit": "ml"},
                   {"name": "Onions", "amount": "2", "unit": None},
                   {"name": "Garclic cloves", "amount": "3", "unit": None},
                   {"name": "Kidney Beans", "amount": "1", "unit": "can"},
                   {"name": "Red pepper", "amount": "1", "unit": None},
                   {"name": "Beef stock cube", "amount": "1", "unit": None},
                   {"name": "Sweetcorn", "amount": "1", "unit": "can"},
                   ]

    def add_meal(name, url, image, instructions):
        m = Meal.objects.get_or_create(user=test_user, name=name)[0]
        if url is not None:
            m.url = url
        if image is not None:
            m.image = f'meal_images/{image}'
        if instructions is not None:
            m.instructions = instructions
        m.save()
        return m

    def add_ingredient(meal, name, amount, unit):
        i = Ingredient.objects.get_or_create(name=name)[0]
        if amount is not None:
            i.amount = amount
        if unit is not None:
            i.unit = unit
        i.save()
        meal.ingredients.add(i)
        return i

    # add Meals
    for m in meals:
        add_meal(m["name"], m["url"], m["image"], m["instructions"])

    # add Ingredients
    for i in spaghetti_ingredients:
        add_ingredient(Meal.objects.get(name="Spaghetti Bolognese"), i["name"], i["amount"], i["unit"])
    for i in chili_ingredients:
        add_ingredient(Meal.objects.get(name="Chili con Carne"), i["name"], i["amount"], i["unit"])

    # add ingredients to shopping list
    if not ShoppingListItem.objects.all().exists():
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
