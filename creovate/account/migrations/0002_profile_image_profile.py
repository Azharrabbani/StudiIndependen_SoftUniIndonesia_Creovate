# Generated by Django 5.1.3 on 2024-12-07 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='image_profile',
            field=models.ImageField(blank=True, default='profile_icon.png', null=True, upload_to=''),
        ),
    ]
