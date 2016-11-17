# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('subject', models.CharField(max_length=100)),
                ('message', models.TextField()),
                ('read', models.BooleanField()),
                ('encrypted', models.BooleanField()),
                ('sent', models.DateTimeField(auto_now_add=True)),
                ('sender', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='message_from')),
                ('to', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='message_to')),
            ],
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('name', models.CharField(default='GROUP', serialize=False, max_length=100, primary_key=True)),
                ('members', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
