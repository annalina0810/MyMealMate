from django import forms
from django.contrib.auth.models import User
from MyMealMate.models import UserProfile
from MyMealMate.models import Meal

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'password' ,)
        

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture', )


class MealForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the meal name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Meal
        fields = ('name',)
