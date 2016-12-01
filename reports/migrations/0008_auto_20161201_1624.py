# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0007_auto_20161201_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='long_desc',
            field=models.TextField(),
        ),
    ]
