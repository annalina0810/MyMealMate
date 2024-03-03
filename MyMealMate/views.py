from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from MyMealMate.forms import UserForm, UserProfileForm

def home(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:

            if user.is_active:
                login(request, user)
                return redirect(reverse('MyMealMate:user_hub'))
            
            else:
                return HttpResponse("Your MyMealMate account is disabled.")
            
        else:
            print("Invalid login details.")
            return HttpResponse("Invalid login details supplied.")
        
    else:
        return render(request, 'MyMealMate/home.html')

def signup(request):
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
def user_hub(request):
    context_dict = {}
    
    response = render(request, 'MyMealMate/user_hub.html', context = context_dict)
    return response

@login_required
def profile(request):
    context_dict = {}
    
    response = render(request, 'MyMealMate/profile.html', context = context_dict)
    return response

@login_required
def edit_profile(request):
    context_dict = {}
    
    response = render(request, 'MyMealMate/edit_profile.html', context = context_dict)
    return response

@login_required
def my_meals(request):
    context_dict = {}
    
    response = render(request, 'MyMealMate/my_meals.html', context = context_dict)
    return response

@login_required
def new_meal(request):
    context_dict = {}
    
    response = render(request, 'MyMealMate/new_meal.html', context = context_dict)
    return response

@login_required
def meal(request):
    context_dict = {}
    
    response = render(request, 'MyMealMate/meal.html', context = context_dict)
    return response

@login_required
def edit_meal(request):
    context_dict = {}
    
    response = render(request, 'MyMealMate/edit_meal.html', context = context_dict)
    return response

@login_required
def shopping_list(request):
    context_dict = {}
    
    response = render(request, 'MyMealMate/shopping_list.html', context = context_dict)
    return response

@login_required
def edit_shopping_list(request):
    context_dict = {}
    
    response = render(request, 'MyMealMate/edit_shopping_list.html', context = context_dict)
    return response

@login_required
def schedule(request):
    context_dict = {}
    
    response = render(request, 'MyMealMate/schedule.html', context = context_dict)
    return response