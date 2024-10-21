# Generated by Django 5.1.2 on 2024-10-21 08:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0005_alter_category_slug_alter_tea_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tea",
            name="rating",
            field=models.PositiveIntegerField(
                default=1,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(5),
                ],
            ),
        ),
    ]