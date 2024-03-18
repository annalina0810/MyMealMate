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
    path('my_meals/<slug:meal_name_slug>/', views.meal, name='meal'),
    path('my_meals/<slug:meal_name_slug>/edit_meal/', views.edit_meal, name='edit_meal'),
    path('my_meals/<slug:meal_name_slug>/delete_meal/', views.delete_meal, name='delete_meal'),
    path('mymeals/<slug:meal_name_slug>/add_ingredient/', views.add_ingredient, name='add_ingredient'),
    path('mymeals/<slug:meal_name_slug>/delete_ingredient/', views.delete_ingredient, name='delete_ingredient'),
    path('mymeals/<slug:meal_name_slug>/edit_ingredient/', views.edit_ingredient, name='edit_ingredient'),
    path('user_hub/add_meal_of_the_day/', views.add_meal_of_the_day, name='add_meal_of_the_day'),
    path('schedule/', views.schedule, name='schedule'),
    path('shopping_list/', views.shopping_list, name='shopping_list'),
    path('shopping_list/clear_all', views.clear_all, name='clear_all'),
    path('shopping_list/clear_completed/', views.clear_completed, name='clear_completed'),
    path('shopping_list/clicked/<int:item_id>/', views.clicked_item, name='clicked'),
    path('shopping_list/edit_shopping_list/', views.edit_shopping_list, name='edit_shopping_list'),
    path('shopping_list/edit_shopping_list/add_item', views.add_shopping_list_item, name='add_item'),
    path('shopping_list/edit_shopping_list/edit_item', views.edit_shopping_list_item, name='edit_item'),
    path('shopping_list/edit_shopping_list/delete_item', views.delete_shopping_list_item, name='delete_item'),
    path('logout/', views.user_logout, name='logout'),
    path('delete_account/', views.delete_account, name="delete_account"),
]