# Generated by Django 5.1.3 on 2024-12-09 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0005_alter_service_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
