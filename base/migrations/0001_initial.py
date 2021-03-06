# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-16 16:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eid', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gid', models.CharField(max_length=38)),
                ('name', models.CharField(max_length=512)),
                ('year', models.IntegerField(blank=True, null=True)),
                ('developer', models.CharField(blank=True, max_length=512, null=True)),
                ('publisher', models.CharField(blank=True, max_length=512, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('reg_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
