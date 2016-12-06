# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0012_auto_20161204_0013'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='file_encrypted',
            field=models.BooleanField(default=False),
        ),
    ]
