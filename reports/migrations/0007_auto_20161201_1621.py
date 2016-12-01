# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('web', '0002_auto_20161114_0341'),
        ('reports', '0006_auto_20161129_1918'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='username',
        ),
        migrations.AddField(
            model_name='report',
            name='group',
            field=models.ForeignKey(blank=True, null=True, to='web.UserGroup'),
        ),
        migrations.AddField(
            model_name='report',
            name='owner',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
