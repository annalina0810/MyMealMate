from django.urls import path
from MyMealMate import views

app_name = 'MyMealMate'

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('user_hub/', views.user_hub, name='user_hub'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit_profile/', views.edit_profile, name='edit_profile'),
    path('my_meals/', views.my_meals, name='my_meals'),
    path('my_meals/new_meal/', views.new_meal, name='new_meal'),
    path('user_hub/add_meal_of_the_day/', views.add_meal_of_the_day, name='add_meal_of_the_day'),
    path('my_meals/<slug:meal_name_slug>/', views.meal, name='meal'),
    path('my_meals/<slug:meal_name_slug>/edit_meal/', views.edit_meal, name='edit_meal'),
    path('schedule/', views.schedule, name='schedule'),
    path('shopping_list/', views.shopping_list, name='shopping_list'),
    path('shopping_list/clear_all', views.clear_all, name='clear_all'),
    path('shopping_list/clear_completed/', views.clear_completed, name='clear_completed'),
    path('shopping_list/clicked/<int:item_id>/', views.clicked_item, name='clicked'),
    path('shopping_list/edit_shopping_list/', views.edit_shopping_list, name='edit_shopping_list'),
    path('logout/', views.user_logout, name='logout'),
    path('delete_account/', views.delete_account, name="delete_account"),
]