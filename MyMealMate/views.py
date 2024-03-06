from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from MyMealMate.forms import UserForm, UserProfileForm, MealForm, EditProfileForm, EditPictureForm
from MyMealMate.models import *
import datetime


def home(request):
    context_dict = {'nbar': 'home'}

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

    context_dict = {'user_form': user_form,
                    'profile_form':profile_form,
                    'registered': registered,}
    
    response = render(request, 'MyMealMate/signup.html', context = context_dict)
    return response

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('MyMealMate:home'))

@login_required
def delete_account(request):

    user = request.user
    user.delete()
    return redirect(reverse('MyMealMate:home'))

@login_required
def user_hub(request):
    context_dict = {'nbar': 'user_hub',
                    'user': request.user}
    
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
            return redirect('/MyMealMate/my_meals/')
    else:
        print(form.errors)

    return render(request, 'MyMealMate/new_meal.html', {'form': form})


@login_required
def meal(request):
    context_dict = {'nbar': 'meal'}
    
    response = render(request, 'MyMealMate/meal.html', context = context_dict)
    return response

@login_required
def edit_meal(request):
    context_dict = {'nbar': 'edit_meal'}
    
    response = render(request, 'MyMealMate/edit_meal.html', context = context_dict)
    return response

@login_required
def shopping_list(request):
    context_dict = {'nbar': 'shopping_list'}
    
    response = render(request, 'MyMealMate/shopping_list.html', context = context_dict)
    return response

@login_required
def edit_shopping_list(request):
    context_dict = {'nbar': 'shopping_list'}
    
    response = render(request, 'MyMealMate/edit_shopping_list.html', context = context_dict)
    return response

@login_required
def schedule(request):
    context_dict = {'nbar': 'schedule'}
    
    response = render(request, 'MyMealMate/schedule.html', context = context_dict)
    return response