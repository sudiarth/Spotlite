# Generated by Django 2.0.6 on 2018-06-25 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_spotlite', '0002_user_profilepic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=128),
        ),
    ]