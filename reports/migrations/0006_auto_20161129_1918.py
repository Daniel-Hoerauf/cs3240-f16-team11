# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0005_folder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='files',
            field=models.FileField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='report',
            name='private',
            field=models.BooleanField(default=False),
        ),
    ]
