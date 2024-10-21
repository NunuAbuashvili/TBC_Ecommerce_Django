# Generated by Django 5.1.2 on 2024-10-20 07:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, unique=True)),
                (
                    "description",
                    models.TextField(
                        blank=True, null=True, verbose_name="category description"
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "Category",
                "verbose_name_plural": "Categories",
            },
        ),
        migrations.CreateModel(
            name="Tea",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(verbose_name="product description")),
                ("manufacturer", models.CharField(max_length=100)),
                (
                    "place_of_origin",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "ingredients",
                    models.TextField(blank=True, null=True, verbose_name="ingredients"),
                ),
                ("price", models.DecimalField(decimal_places=2, max_digits=7)),
                ("stock_quantity", models.PositiveIntegerField(default=0)),
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to="products/"),
                ),
                ("rating", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="products",
                        to="store.category",
                    ),
                ),
            ],
        ),
    ]
