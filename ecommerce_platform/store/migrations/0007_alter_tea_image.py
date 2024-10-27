# Generated by Django 5.1.2 on 2024-10-23 19:05

import versatileimagefield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0006_alter_tea_rating"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tea",
            name="image",
            field=versatileimagefield.fields.VersatileImageField(
                blank=True, null=True, upload_to="products/", verbose_name="Image"
            ),
        ),
    ]