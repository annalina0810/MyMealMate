from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.conf import settings


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_images', blank=True, default="default_profile.jpg")
    schedule = models.OneToOneField('Schedule', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.user.username

class Ingredient(models.Model):
    name = models.CharField(max_length=30)
    amount = models.IntegerField(blank=True, null=True)
    unit = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Meal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to="meal_images/", null=True, blank=True)  
    ingredients = models.ManyToManyField(Ingredient)
    url = models.URLField(blank=True)
    instructions = models.TextField(blank=True)
    schedCounter = models.IntegerField(default=0)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        if not self.slug or Meal.objects.filter(slug=self.slug).exists():
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Meal.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super(Meal, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Meals'

    def __str__(self):
        return self.name

class ShoppingList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def add_item(self, name, amount, unit):
        initial_items = ShoppingListItem.objects.filter(shoppingList=self, name=name)

        for item in initial_items:  # iterate over all items with the same name
            if item.unit == unit and not item.checked:  # if one of them has the same unit, add the amount
                item.amount += amount
                item.save()
                return item

        # if we didn't find another item with the same name & unit, add a new ShoppingListItem
        new_item = ShoppingListItem(shoppingList=self, name=name, amount=amount, unit=unit)

        new_item.save()
        return new_item

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
