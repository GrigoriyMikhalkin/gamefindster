# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-18 13:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_auto_20160218_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='cover',
            field=models.FileField(default='/media/games/covers/not_available.gif', upload_to='/media/games/covers/'),
        ),
    ]
