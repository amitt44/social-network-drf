# Generated by Django 4.1.2 on 2022-10-27 08:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('siimapp', '0003_favoritepost_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FavoritePost',
        ),
    ]
