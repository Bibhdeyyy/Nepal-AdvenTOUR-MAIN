# Generated by Django 5.0.2 on 2024-02-21 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_remove_user_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='connect',
            field=models.CharField(choices=[('no', 'No'), ('yes', 'Yes')], max_length=10),
        ),
    ]
