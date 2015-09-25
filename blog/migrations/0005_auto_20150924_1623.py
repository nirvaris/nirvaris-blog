# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20150924_1616'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='is_active',
            new_name='is_approved',
        ),
    ]
