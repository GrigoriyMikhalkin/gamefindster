# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-19 14:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_delete_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date started'),
        ),
    ]