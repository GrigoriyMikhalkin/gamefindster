# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-19 14:52
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_auto_20160219_1409'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='description',
            field=ckeditor.fields.RichTextField(default='test', verbose_name='description'),
            preserve_default=False,
        ),
    ]
