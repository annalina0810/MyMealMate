from django import forms
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from MyMealMate.models import UserProfile
from MyMealMate.models import Meal, ShoppingListItem, Ingredient

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

class MealEditForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ('name', 'image', 'url', 'instructions', )

class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ('name', 'image', 'url', )

    def __init__(self, *args, **kwargs):
        super(MealForm, self).__init__(*args, **kwargs)
        self.fields['name'].unique = False
        self.fields['name'].label = 'Name (required):'
        self.fields['url'].label = 'Recipe URL:'

    def save(self, commit=True):
        meal = super().save(commit=False)
        if not self.cleaned_data.get('image'):
            meal.image = "default_meal_image.jpg"
        if commit:
            meal.save()
        return meal

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ('name', 'amount', 'unit',)

class ShoppingListForm(forms.ModelForm):
    name = forms.CharField(max_length=30, help_text="Name:")
    amount = forms.IntegerField(help_text="Amount:", required=False, min_value=0)
    unit = forms.CharField(max_length=30, help_text="Unit:", required=False)
    checked = forms.BooleanField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = ShoppingListItem
        fields = ('name', "amount", "unit", "checked",)
