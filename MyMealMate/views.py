from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.views.decorators.csrf import csrf_exempt
from django.template.defaultfilters import slugify
from MyMealMate.forms import *
from MyMealMate.models import *
from MyMealMate.forms import MealForm, MealEditForm
from datetime import datetime,timedelta
from http import client
from http import cookiejar
import json
import http
from fractions import Fraction
import re
from django.core.files.base import ContentFile
import os
import urllib.request

def home(request):
    context_dict = {'nbar': 'home'}
    set_meal_cookie(request)
    context_dict['meal_of_the_day'] = request.session['meal_of_the_day']

    if request.user.is_authenticated:
        return redirect(reverse('MyMealMate:user_hub'))

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:

            if user.is_active:
                login(request, user)
                return redirect(reverse('MyMealMate:user_hub'))
            
            else:
                context_dict['error_message'] = "Your MyMealMate account is disabled."
                return render(request, 'MyMealMate/home.html', context=context_dict)

        else:
            print("Invalid login details.")
            context_dict['error_message'] = "Invalid login details supplied."
            return render(request, 'MyMealMate/home.html', context=context_dict)

    else:
        return render(request, 'MyMealMate/home.html', context=context_dict)


def signup(request):
    context_dict = {'nbar': 'signup'}

    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True
            login(request, user)

            return redirect(reverse('MyMealMate:user_hub'))
        else:
            print(user_form.errors, profile_form.errors)
    
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    set_meal_cookie(request)
    context_dict = {'user_form': user_form,
                    'profile_form':profile_form,
                    'registered': registered,
                    'meal_of_the_day': request.session['meal_of_the_day']}

    response = render(request, 'MyMealMate/signup.html', context = context_dict)
    return response


@login_required
def user_logout(request):
    meal_of_the_day = request.session.get('meal_of_the_day', None)
    last_set = request.session.get('last_set', None)
    logout(request)
    request.session['meal_of_the_day'] = meal_of_the_day
    request.session['last_set'] = last_set
    return redirect(reverse('MyMealMate:home'))


@login_required
def delete_account(request):
    user = request.user
    user.delete()
    return redirect(reverse('MyMealMate:home'))


@login_required
def user_hub(request):
    set_meal_cookie(request)
    meal_of_the_day = request.session['meal_of_the_day']
    context_dict = {'nbar': 'user_hub',
                    'user': request.user,
                    'meal_of_the_day': meal_of_the_day,
                    'has_meal_of_the_day': userHasMeal(request,meal_of_the_day['strMeal'])}
    response = render(request, 'MyMealMate/user_hub.html', context = context_dict)
    return response


@login_required
def profile(request):
    user = request.user
    picture = UserProfile.objects.get(user=user).picture
    context_dict = {'nbar': 'profile', 
                    'user': user,
                    'profile_picture': picture}
    
    response = render(request, 'MyMealMate/profile.html', context = context_dict)
    return response


@login_required
def edit_profile(request):
    user = request.user
    userProfile = UserProfile.objects.get(user=user)
        
    if request.method == "POST":
        profile_form = EditProfileForm(request.POST, instance=user)
        picture_form = EditPictureForm(request.POST, instance=userProfile)

        if profile_form.is_valid() and picture_form.is_valid():

            if 'picture' in request.FILES:
                userProfile.picture = request.FILES['picture']
            else:
                userProfile.picture = "default_profile.jpg"

            profile_form.save()
            picture_form.save()
            return redirect(reverse('MyMealMate:profile'))
    
    else:
        profile_form = EditProfileForm(instance=user)
        picture_form = EditPictureForm(instance=userProfile)

    context_dict = {'nbar': 'profile',
                    'user': user,
                    'profile_picture': userProfile.picture,
                    'edit_profile_form': profile_form,
                    'edit_picture_form': picture_form,}
    
    response = render(request, 'MyMealMate/edit_profile.html', context = context_dict)
    return response


@login_required
def my_meals(request):
    context_dict = {'nbar': 'my_meals'}
  
    meals = Meal.objects.filter(user=request.user)
    context_dict["meals"] = meals
    context_dict["username_slug"] = slugify(request.user.username)

    response = render(request, 'MyMealMate/my_meals.html', context=context_dict)
    return response


@login_required
def new_meal(request):

    if request.method == 'POST':
        form = MealForm(request.POST, request.FILES)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.user = request.user  
            meal.save()
            return redirect(reverse('MyMealMate:my_meals'))
    else:
        form = MealForm()

    return render(request, 'MyMealMate/new_meal.html', {'form': form})


@login_required
def meal(request, meal_name_slug):
    meal = Meal.objects.filter(user=request.user).get(slug=meal_name_slug)
    context_dict = {'nbar': 'meal', "meal": meal, "username_slug": slugify(request.user.username)}

    """"
    # this is how you'd schedule/unschedule a meal for tomorrow
    user_schedule = Schedule.objects.get(user=request.user)
    tomorrow = Day(schedule=user_schedule, date=datetime.date.today() + datetime.timedelta(days=1))
    tomorrow.save()
    user_schedule.scheduleMeal(tomorrow, meal)
    #user_schedule.unscheduleMeal(tomorrow, meal)
    user_schedule.save()
    """
    response = render(request, 'MyMealMate/meal.html', context = context_dict)
    return response


def edit_meal(request, meal_name_slug):
    meal = get_object_or_404(Meal, slug=meal_name_slug, user=request.user)

    if request.method == 'POST':
        form = MealEditForm(request.POST, request.FILES, instance=meal)
        if form.is_valid():
            meal = form.save(commit=False)
            # Save the meal and retrieve the updated ingredients list
            ingredients_list = request.POST.getlist('ingredients')
            meal.save()
            return render(request, 'MyMealMate/meal.html', {'meal': meal, 'ingredients_list': ingredients_list})
    else:
        form = MealEditForm(instance=meal)
    return render(request, 'MyMealMate/edit_meal.html', {'form': form, 'meal': meal})

@csrf_exempt
def add_ingredient(request, meal_name_slug):
    if request.method == 'POST':
        name = request.POST.get('name')
        amount = request.POST.get('amount')
        unit = request.POST.get('unit')
        meal = get_object_or_404(Meal, slug=meal_name_slug, user=request.user)

        # Create the new ingredient and associate it with the meal
        ingredient = Ingredient.objects.create(name=name, amount=amount, unit=unit)
        meal.ingredients.add(ingredient)

        return JsonResponse({'id': ingredient.id})

@csrf_exempt
def edit_ingredient(request, meal_name_slug):
    if request.method == 'GET':
        ingredient_id = request.GET.get('ingredient_id')
        try:
            ingredient = Ingredient.objects.get(id=ingredient_id)
            data = {
                'name': ingredient.name,
                'amount': ingredient.amount,
                'unit': ingredient.unit
            }
            response = JsonResponse(data)
            
            return response
        except Ingredient.DoesNotExist:
            return JsonResponse({'error': 'Ingredient not found'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def delete_ingredient(request, meal_name_slug):
    if request.method == 'POST':
        # Retrieve the meal
        meal = get_object_or_404(Meal, slug=meal_name_slug, user=request.user)
        ingredient_id = request.POST.get('ingredient_id')
        # Retrieve the ingredient
        ingredient = get_object_or_404(Ingredient, id=ingredient_id)
        
        # Remove the ingredient from the meal
        meal.ingredients.remove(ingredient)
        
        # Delete the ingredient itself
        ingredient.delete()
        
        return JsonResponse({'message': 'Ingredient deleted successfully'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
def delete_meal(request, meal_name_slug):
    meal = get_object_or_404(Meal, slug=meal_name_slug)

    if request.method == 'POST':
        meal.delete()

    return redirect(reverse('MyMealMate:my_meals'))

@login_required
def shopping_list(request):
    shopping_list = ShoppingList.objects.get_or_create(user=request.user)[0]
    items = ShoppingListItem.objects.filter(shoppingList=shopping_list).order_by("checked")

    context_dict = {'nbar': 'shopping_list', "items": items}
    response = render(request, 'MyMealMate/shopping_list.html', context = context_dict)
    return response


@login_required
def clicked_item(request, item_id):
    item = ShoppingListItem.objects.get(id=item_id)

    if request.method == 'POST':
        item.checked = not item.checked
        item.save()
        return redirect(reverse('MyMealMate:shopping_list'))

    return render(request, 'MyMealMate/shopping_list.html')


@login_required
def clear_all(request):
    shopping_list = ShoppingList.objects.get(user=request.user)
    ShoppingListItem.objects.filter(shoppingList=shopping_list).delete()

    return redirect(reverse('MyMealMate:shopping_list'))


@login_required
def clear_completed(request):
    shopping_list = ShoppingList.objects.get(user=request.user)
    ShoppingListItem.objects.filter(shoppingList=shopping_list, checked=True).delete()

    return redirect(reverse('MyMealMate:shopping_list'))


@login_required
def edit_shopping_list(request):
    # ToDo: don't allow unit without amount
    shopping_list = ShoppingList.objects.get_or_create(user=request.user)[0]
    items = ShoppingListItem.objects.filter(shoppingList=shopping_list).order_by("checked")
    form = ShoppingListForm()

    if request.method == 'POST':
        form = ShoppingListForm(request.POST)
        if form.is_valid():
            amount = int(form.data["amount"]) if form.data["amount"] != "" else 0
            item = shopping_list.add_item(form.data['name'], amount, form.data["unit"])

            return redirect(reverse('MyMealMate:edit_shopping_list'))
    else:
        print(form.errors)

    context_dict = {'nbar': 'shopping_list', "items": items, "form": form}

    response = render(request, 'MyMealMate/edit_shopping_list.html', context = context_dict)
    return response


@login_required
def schedule(request):
    context_dict = {'nbar': 'schedule'}
    
    response = render(request, 'MyMealMate/schedule.html', context = context_dict)
    return response

@login_required
def add_meal_of_the_day(request):
    meal_of_the_day = request.session.get('meal_of_the_day', None)
    if not userHasMeal(request,meal_of_the_day['strMeal']):
        meal = Meal()
        meal.user = request.user
        meal.name = meal_of_the_day['strMeal']
        if meal_of_the_day['strMealThumb']:
            image_url = meal_of_the_day['strMealThumb']
            image_name, image_content = downloadImage(image_url)
            if image_name and image_content:
                meal.image.save(image_name, ContentFile(image_content), save=True)
        if meal_of_the_day['strSource']:
            meal.url = meal_of_the_day['strSource']
        if meal_of_the_day['strInstructions']:
            meal.instructions = meal_of_the_day['strInstructions']
        meal.save()
        for i in meal_of_the_day['ingredients']:
            ingredient = Ingredient.objects.create(name=i['name'], amount=i['amount'], unit=i['unit'])
            meal.ingredients.add(ingredient)
        return redirect(reverse('MyMealMate:my_meals'))
    return redirect(reverse('MyMealMate:user_hub'))

def downloadImage(image_url):
    image_name,image_content = None,None
    try:
        response = urllib.request.urlopen(image_url)
        if response.status == 200:
            image_content = response.read()
            image_name = os.path.basename(image_url)
        else:
            print("Error: Unable to fetch the image")
    except Exception as e:
        print(f"Error downloading image: {e}")
    return image_name,image_content

@login_required
def userHasMeal(request,meal_name):
    if Meal.objects.filter(user=request.user).filter(name=meal_name).exists():
        return True
    return False

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def set_meal_cookie(request):
    meal_cookie = get_server_side_cookie(request, 'meal_of_the_day', "Creamy Tomato Soup")
    last_set = get_server_side_cookie(request, 'last_set')
    
    if meal_cookie and last_set:
        last_set_timestamp = datetime.strptime(last_set, "%Y-%m-%d %H:%M:%S.%f")
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        if last_set_timestamp >= today_start:
            return None

    conn = http.client.HTTPSConnection("www.themealdb.com")
    conn.request("GET", "/api/json/v1/1/random.php")
    response_from_api = conn.getresponse()

    if response_from_api.status == 200:
        meal = json.loads(response_from_api.read().decode('utf-8'))["meals"][0]
        meal = collect_ingredients(meal)
        request.session['meal_of_the_day'] = meal
        request.session['last_set'] = str(datetime.now())

    conn.close()

def collect_ingredients(meal):
    ingredients = []
    for i in range(1, 21):
        ingredient_key = "strIngredient" + str(i)
        measure_key = "strMeasure" + str(i)
        if meal[ingredient_key] and meal[measure_key]:
            measurement = parse_measurement(meal[measure_key])
            ingredient = {
                "name":meal[ingredient_key],
                "amount":measurement["amount"],
                "unit":measurement["unit"],
            }
            ingredients.append(ingredient)
        else:
            break

    return {
        "idMeal": meal["idMeal"],
        "strMeal": meal["strMeal"],
        "strDrinkAlternate": meal["strDrinkAlternate"],
        "strCategory": meal["strCategory"],
        "strArea": meal["strArea"],
        "strInstructions": meal["strInstructions"],
        "strMealThumb": meal["strMealThumb"],
        "strTags": meal["strTags"],
        "strYoutube": meal["strYoutube"],
        "ingredients": ingredients,
        "strSource": meal["strSource"],
        "strImageSource": meal["strImageSource"],
        "strCreativeCommonsConfirmed": meal["strCreativeCommonsConfirmed"],
        "dateModified": meal["dateModified"]
    }

def parse_measurement(measurement):
    amount = 1
    unit = ""
    if measurement.isspace():
        return {"amount": amount, "unit": unit}
    regex = r"(\d+\s+\d+/\d+)|(\d+/\d+)|(\d+\.\d+)|(\d+)|(\D+)"
    matches = re.findall(regex, measurement)
    if all((bool(match[-1]) and all(not m for m in match[:-1])) for match in matches):
            return {"amount": 1, "unit": "".join(match[-1] for match in matches)}
    def switch(case):
        switcher = {
            0: lambda s: float(s.split(' ')[0]) + Fraction(s.split(' ')[1]),
            1: lambda s: float(Fraction(s)),
            2: lambda s: float(s),
            3: lambda s: int(s)
        }
        return switcher[case]
    for match in matches:
        for i in range(4):
            if match[i]:
                amount = switch(i)(match[i])
        if match[4]:
            unit += match[4]
    return {"amount": amount, "unit": unit}