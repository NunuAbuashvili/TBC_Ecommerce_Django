# Generated by Django 5.1.2 on 2024-11-06 08:38

import django_countries.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0005_customuser_last_active_datetime"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="account_type_en",
            field=models.CharField(
                choices=[("individual", "Individual"), ("company", "Company")],
                default="individual",
                max_length=20,
                null=True,
                verbose_name="account type",
            ),
        ),
        migrations.AddField(
            model_name="customuser",
            name="account_type_ka",
            field=models.CharField(
                choices=[("individual", "Individual"), ("company", "Company")],
                default="individual",
                max_length=20,
                null=True,
                verbose_name="account type",
            ),
        ),
        migrations.AddField(
            model_name="customuser",
            name="city_en",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="city"
            ),
        ),
        migrations.AddField(
            model_name="customuser",
            name="city_ka",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="city"
            ),
        ),
        migrations.AddField(
            model_name="customuser",
            name="country_en",
            field=django_countries.fields.CountryField(max_length=2, null=True),
        ),
        migrations.AddField(
            model_name="customuser",
            name="country_ka",
            field=django_countries.fields.CountryField(max_length=2, null=True),
        ),
        migrations.AddField(
            model_name="customuser",
            name="gender_en",
            field=models.CharField(
                choices=[
                    ("M", "Male"),
                    ("F", "Female"),
                    ("O", "Other"),
                    ("P", "Prefer Not To Say"),
                ],
                default="P",
                max_length=2,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="customuser",
            name="gender_ka",
            field=models.CharField(
                choices=[
                    ("M", "Male"),
                    ("F", "Female"),
                    ("O", "Other"),
                    ("P", "Prefer Not To Say"),
                ],
                default="P",
                max_length=2,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="customuser",
            name="street_address_en",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="street address"
            ),
        ),
        migrations.AddField(
            model_name="customuser",
            name="street_address_ka",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="street address"
            ),
        ),
    ]
