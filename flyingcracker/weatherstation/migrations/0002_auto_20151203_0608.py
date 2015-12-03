# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weatherstation', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='weather',
            options={'ordering': ['timestamp'], 'get_latest_by': 'timestamp'},
        ),
    ]
