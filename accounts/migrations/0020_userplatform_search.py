# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-04-01 00:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_auto_20160331_1603'),
    ]

    operations = [
        migrations.AddField(
            model_name='userplatform',
            name='search',
            field=models.BooleanField(default=False),
        ),
    ]