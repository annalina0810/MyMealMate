from django import forms
from django.template.defaultfilters import slugify
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
    name = forms.CharField(max_length=30, help_text="Please enter the meal name.")
    url = forms.URLField(required=False, help_text="url:")
    instructions = forms.CharField(max_length=500, required=False, help_text="instructions")
    schedCounter = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(MealForm, self).__init__(*args, **kwargs)
        self.user = user

    def clean_name(self):
        cleaned_data = self.clean()
        name = cleaned_data.get('name')
        if Meal.objects.filter(user=self.user, slug=slugify(name)).exists():
            self.add_error('name', "You have already a meal with that name")
        return name

    class Meta:
        model = Meal
        fields = ('name', 'url', 'instructions', )


class ShoppingListForm(forms.ModelForm):
    name = forms.CharField(max_length=30, help_text="Name:")
    amount = forms.IntegerField(help_text="Amount:", required=False)
    unit = forms.CharField(max_length=30, help_text="Unit:", required=False)
    checked = forms.BooleanField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = ShoppingListItem
        fields = ('name', "amount", "unit", "checked",)
