# Generated by Django 5.0.2 on 2024-04-21 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0006_hotel_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='latitude',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='activity',
            name='longitude',
            field=models.FloatField(default=0.0),
        ),
    ]
