# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-05 18:42
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0017_auto_20160305_1340'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EventApplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='EventNotification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friend', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend_set', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friends', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FriendApplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='FriendNotification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=128)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GroupApplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='GroupNotification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='GroupParticipation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_social.Group')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='date started')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sended', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=64)),
                ('label', models.CharField(max_length=256)),
                ('text', models.TextField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='date started')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Participation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_host', models.BooleanField(default=False)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Event')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='my_social.Notification')),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='groupnotification',
            name='notification',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='group_notification', to='my_social.Notification'),
        ),
        migrations.AddField(
            model_name='groupnotification',
            name='notification_subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_social.Group'),
        ),
        migrations.AddField(
            model_name='groupapplication',
            name='request',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='group_application', to='my_social.Request'),
        ),
        migrations.AddField(
            model_name='groupapplication',
            name='request_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_social.Group'),
        ),
        migrations.AddField(
            model_name='friendnotification',
            name='notification',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='friend_notification', to='my_social.Notification'),
        ),
        migrations.AddField(
            model_name='friendnotification',
            name='notification_subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='friendapplication',
            name='request',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='friend_application', to='my_social.Request'),
        ),
        migrations.AddField(
            model_name='friendapplication',
            name='request_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='eventnotification',
            name='notification',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='event_notification', to='my_social.Notification'),
        ),
        migrations.AddField(
            model_name='eventnotification',
            name='notification_subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Event'),
        ),
        migrations.AddField(
            model_name='eventapplication',
            name='request',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='event_application', to='my_social.Request'),
        ),
        migrations.AddField(
            model_name='eventapplication',
            name='request_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Event'),
        ),
    ]
