# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-31 16:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_auto_20160331_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersearchsettings',
            name='location',
            field=models.CharField(default='300', max_length=32),
        ),
    ]