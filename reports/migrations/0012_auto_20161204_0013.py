# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import reports.models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0011_auto_20161201_1807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='files',
            field=models.FileField(null=True, blank=True, upload_to=reports.models.get_file_dest),
        ),
    ]
