# Generated by Django 2.2.28 on 2024-03-08 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyMealMate', '0004_auto_20240306_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='image',
            field=models.ImageField(upload_to='meal_images/'),
        ),
    ]
