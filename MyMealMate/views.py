from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def home(request):
    context_dict = {'nbar': 'home'}

    response = render(request, 'MyMealMate/home.html', context = context_dict)
    return response

def signup(request):
    context_dict = {'nbar': 'signup'}
    
    response = render(request, 'MyMealMate/signup.html', context = context_dict)
    return response

def user_hub(request):
    context_dict = {'nbar': 'user_hub'}
    
    response = render(request, 'MyMealMate/user_hub.html', context = context_dict)
    return response

def profile(request):
    context_dict = {'nbar': 'profile'}
    
    response = render(request, 'MyMealMate/profile.html', context = context_dict)
    return response

def edit_profile(request):
    context_dict = {'nbar': 'edit_profile'}
    
    response = render(request, 'MyMealMate/edit_profile.html', context = context_dict)
    return response

def my_meals(request):
    context_dict = {'nbar': 'my_meals'}
    
    response = render(request, 'MyMealMate/my_meals.html', context = context_dict)
    return response

def new_meal(request):
    context_dict = {'nbar': 'new_meal'}
    
    response = render(request, 'MyMealMate/new_meal.html', context = context_dict)
    return response

def meal(request):
    context_dict = {'nbar': 'meal'}
    
    response = render(request, 'MyMealMate/meal.html', context = context_dict)
    return response

def edit_meal(request):
    context_dict = {'nbar': 'edit_meal'}
    
    response = render(request, 'MyMealMate/edit_meal.html', context = context_dict)
    return response

def shopping_list(request):
    context_dict = {'nbar': 'shopping_list'}
    
    response = render(request, 'MyMealMate/shopping_list.html', context = context_dict)
    return response

def edit_shopping_list(request):
    context_dict = {'nbar': 'edit_shopping_list'}
    
    response = render(request, 'MyMealMate/edit_shopping_list.html', context = context_dict)
    return response

def schedule(request):
    context_dict = {'nbar': 'schedule'}
    
    response = render(request, 'MyMealMate/schedule.html', context = context_dict)
    return response