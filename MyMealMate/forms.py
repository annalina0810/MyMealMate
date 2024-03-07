from django import forms
from django.contrib.auth.models import User
from MyMealMate.models import UserProfile
from MyMealMate.models import Meal, ShoppingListItem

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'password' ,)
        

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture', )

    def save(self, commit=True):
        userProfile = super().save(commit=False)
        if not self.cleaned_data.get('picture'):
            userProfile.picture = "default_profile.jpg"
        if commit:
            userProfile.save()
        return userProfile

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields =('username', 'first_name', 'email',)

class EditPictureForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)


class MealForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the meal name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Meal
        fields = ('name',)


class ShoppingListForm(forms.ModelForm):
    name = forms.CharField(max_length=30, help_text="Name:")
    amount = forms.IntegerField(help_text="Amount:", required=False)
    unit = forms.CharField(max_length=30, help_text="Unit:", required=False)
    checked = forms.BooleanField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = ShoppingListItem
        fields = ('name', "amount", "unit", "checked",)
