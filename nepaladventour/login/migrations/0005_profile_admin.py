# Generated by Django 5.0.2 on 2024-02-24 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_rename_user_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='admin',
            field=models.BooleanField(default=False),
        ),
    ]
