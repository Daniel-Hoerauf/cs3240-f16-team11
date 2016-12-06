# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0013_report_file_encrypted'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='keyword',
            field=models.CharField(default='', max_length=32),
        ),
    ]
