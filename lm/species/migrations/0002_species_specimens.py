# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('species', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='species',
            name='specimens',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
    ]
