from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from MyMealMate.forms import *
from MyMealMate.models import *
from MyMealMate.forms import MealForm
from datetime import datetime,timedelta
from http import client
from http import cookiejar
import json
import http


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

    response = render(request, 'MyMealMate/my_meals.html', context=context_dict)
    return response


@login_required
def new_meal(request):
    form = MealForm()

    if request.method == 'POST':
        form = MealForm(request.POST)
        if form.is_valid():
            # Save the new meal to the database
            meal = form.save(commit=False)
            meal.user = request.user
            meal.save()
            print(meal, meal.slug)
            return redirect(reverse('MyMealMate:meal', kwargs={'meal_name_slug': meal.slug}))
    else:
        print(form.errors)

    return render(request, 'MyMealMate/new_meal.html', {'form': form})


@login_required
def meal(request, meal_name_slug):
    meal = Meal.objects.filter(user=request.user).get(slug=meal_name_slug)
    context_dict = {'nbar': 'meal', "meal": meal}
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


@login_required
def edit_meal(request, meal_name_slug):
    meal = Meal.objects.filter(user=request.user).get(slug=meal_name_slug)
    context_dict = {'nbar': 'edit_meal', "meal": meal}

    response = render(request, 'MyMealMate/edit_meal.html', context = context_dict)
    return response


@login_required
def shopping_list(request):
    shopping_list = ShoppingList.objects.get(user=request.user)
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
    shopping_list = ShoppingList.objects.get(user=request.user)
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
        meal.image = meal_of_the_day['strMealThumb']
        meal.url = meal_of_the_day['strSource']
        meal.instructions = meal_of_the_day['strInstructions']
        meal.save()
        return redirect(reverse('MyMealMate:my_meals'))
    return redirect(reverse('MyMealMate:user_hub'))

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
        request.session['meal_of_the_day'] = json.loads(response_from_api.read().decode('utf-8'))["meals"][0]
        request.session['last_set'] = str(datetime.now())

    conn.close()   