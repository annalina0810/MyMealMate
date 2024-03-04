from django.contrib import admin
from MyMealMate.models import UserProfile

from MyMealMate.models import Meal

class MealAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

# Register your models here
admin.site.register(Meal, MealAdmin)
