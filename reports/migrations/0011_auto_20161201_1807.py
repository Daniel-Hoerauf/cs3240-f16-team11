# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0010_auto_20161201_1805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='files',
            field=models.FileField(null=True, upload_to='', blank=True),
        ),
    ]
