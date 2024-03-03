from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from MyMealMate.models import *
from MyMealMate.forms import MealForm
import datetime


def home(request):
    context_dict = {}

    response = render(request, 'MyMealMate/home.html', context=context_dict)
    return response


def signup(request):
    context_dict = {}

    response = render(request, 'MyMealMate/signup.html', context=context_dict)
    return response


def user_hub(request):
    context_dict = {}

    response = render(request, 'MyMealMate/user_hub.html', context=context_dict)
    return response


def profile(request):
    context_dict = {}

    response = render(request, 'MyMealMate/profile.html', context=context_dict)
    return response


def edit_profile(request):
    context_dict = {}

    response = render(request, 'MyMealMate/edit_profile.html', context=context_dict)
    return response


def my_meals(request):
    context_dict = {}
    meals = Meal.objects.all()
    context_dict["meals"] = meals

    # see if scheduling and unscheduling works:
    user = get_user_model().objects.filter(username='test_user')[0]
    user_schedule = Schedule.objects.get(user=user)
    today = Day.objects.all()[0]
    tomorrow = Day(schedule=user_schedule, date=datetime.date.today() + datetime.timedelta(days=1))
    tomorrow.save()
    user_schedule.scheduleMeal(tomorrow, meals.get(name="Spaghetti Bolognese"))
    print(user_schedule.unscheduleMeal(today, meals.get(name="Pizza")))
    user_schedule.save()

    response = render(request, 'MyMealMate/my_meals.html', context=context_dict)
    return response


def new_meal(request):
    form = MealForm()

    if request.method == 'POST':
        form = MealForm(request.POST)
        if form.is_valid():
            # Save the new meal to the database
            cat = form.save(commit=True)
            print(cat, cat.slug)
            return redirect('/MyMealMate/')
    else:
        print(form.errors)

    return render(request, 'MyMealMate/new_meal.html', {'form': form})


def meal(request):
    context_dict = {}

    response = render(request, 'MyMealMate/meal.html', context=context_dict)
    return response


def edit_meal(request):
    context_dict = {}

    response = render(request, 'MyMealMate/edit_meal.html', context=context_dict)
    return response


def shopping_list(request):
    context_dict = {}

    response = render(request, 'MyMealMate/shopping_list.html', context=context_dict)
    return response


def edit_shopping_list(request):
    context_dict = {}

    response = render(request, 'MyMealMate/edit_shopping_list.html', context=context_dict)
    return response


def schedule(request):
    context_dict = {}

    response = render(request, 'MyMealMate/schedule.html', context=context_dict)
    return response
