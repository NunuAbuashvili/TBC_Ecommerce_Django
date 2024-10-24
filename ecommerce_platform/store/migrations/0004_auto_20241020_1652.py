# Generated by Django 5.1.2 on 2024-10-20 12:52
from django.db import migrations
from django.utils.text import slugify


def generate_slugs(apps, schema_editor):
    Category = apps.get_model('store', 'Category')
    Tea = apps.get_model('store', 'Tea')

    for category in Category.objects.all():
        category.slug = slugify(category.name)
        category.save()

    for tea in Tea.objects.all():
        tea.slug = slugify(tea.name)
        tea.save()

class Migration(migrations.Migration):

    dependencies = [
        ("store", "0003_category_slug_tea_slug"),
    ]

    operations = [
        migrations.RunPython(generate_slugs),
    ]
