# Generated by Django 2.2.28 on 2024-03-12 23:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MyMealMate', '0009_auto_20240312_2318'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meal',
            name='user',
        ),
    ]
