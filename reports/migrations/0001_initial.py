# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-07 21:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32)),
                ('timestamp', models.DateTimeField(verbose_name='date created')),
                ('short_desc', models.CharField(max_length=100)),
                ('long_desc', models.CharField(max_length=256)),
                ('files', models.CharField(max_length=500)),
                ('private', models.BooleanField()),
            ],
        ),
    ]
