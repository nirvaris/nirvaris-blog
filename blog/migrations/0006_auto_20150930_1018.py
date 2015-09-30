# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20150924_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='last_modified',
            field=models.DateTimeField(default='2015-09-30', auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, blank=True, related_name='post_comments'),
        ),
    ]
