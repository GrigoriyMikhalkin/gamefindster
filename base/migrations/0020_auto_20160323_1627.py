# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-23 16:27
from __future__ import unicode_literals

from django.db import migrations
import stdimage.models
import stdimage.utils


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0019_auto_20160323_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='platform',
            name='logo',
            field=stdimage.models.StdImageField(upload_to=stdimage.utils.UploadToUUID(path='platforms/logo/')),
        ),
    ]
