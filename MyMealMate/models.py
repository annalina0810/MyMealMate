from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.conf import settings


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    picture = models.ImageField(upload_to='profile_images', blank=True, default="default_profile.jpg")

    def __str__(self):
        return self.user.username


class Meal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to="meal_images", blank=True)  # change to blank=False?
    url = models.URLField(blank=True)
    instructions = models.TextField(blank=True)
    schedCounter = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Meal, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Meals'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    amount = models.IntegerField(blank=True, null=True)
    unit = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.name


class ShoppingList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def add_item(self, name, amount, unit):
        initial_items = ShoppingListItem.objects.filter(shoppingList=self, name=name)

        for item in initial_items:  # iterate over all items with the same name
            if item.unit == unit:  # if one of them has the same unit, add the amount
                item.amount += amount
                return item.save()

        # if we didn't find another item with the same name & unit, add a new ShoppingListItem
        new_item = ShoppingListItem(shoppingList=self, name=name, amount=amount, unit=unit)
        return new_item.save()

    def add_ingredient(self, ingredient):
        return self.add_item(ingredient.name, ingredient.amount, ingredient.unit)


class ShoppingListItem(models.Model):
    shoppingList = models.ForeignKey(ShoppingList, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    amount = models.IntegerField(blank=True, null=True)
    unit = models.CharField(max_length=30, blank=True)
    checked = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Schedule(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def scheduleMeal(self, day, meal):
        day.scheduledMeals.add(meal)
        meal.schedCounter += 1
        day.save()
        meal.save()

    def unscheduleMeal(self, day, meal):
        if meal in day.scheduledMeals.all():
            day.scheduledMeals.remove(meal)
            meal.schedCounter -= 1
            day.save()
            meal.save()
        else:
            return "The meal wasn't even scheduled lol"


class Day(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    date = models.DateField()
    scheduledMeals = models.ManyToManyField(Meal)
