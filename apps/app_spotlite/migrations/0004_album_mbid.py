# Generated by Django 2.0.6 on 2018-06-26 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_spotlite', '0003_auto_20180626_1128'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='mbid',
            field=models.CharField(default=1, max_length=64),
            preserve_default=False,
        ),
    ]