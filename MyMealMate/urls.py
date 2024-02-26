from django.urls import path
from MyMealMate import views

app_name = 'MyMealMate'

urlpatterns = [
    path('', views.index, name='index'),
]