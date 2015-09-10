# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metatag',
            name='content',
            field=models.CharField(max_length=70, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='metatag',
            name='property',
            field=models.CharField(max_length=70, blank=True, null=True),
        ),
    ]
