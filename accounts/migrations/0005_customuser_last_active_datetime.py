# Generated by Django 5.1.2 on 2024-10-30 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_alter_customuser_country"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="last_active_datetime",
            field=models.DateTimeField(auto_now=True, verbose_name="last active"),
        ),
    ]
