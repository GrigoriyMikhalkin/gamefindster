# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-27 18:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20160326_1817'),
    ]

    operations = [
        migrations.AddField(
            model_name='languagetouser',
            name='search',
            field=models.BooleanField(default=False),
        ),
    ]