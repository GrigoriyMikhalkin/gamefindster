# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-20 11:13
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_auto_20160219_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='description',
            field=ckeditor.fields.RichTextField(default='This is test description'),
            preserve_default=False,
        ),
    ]
