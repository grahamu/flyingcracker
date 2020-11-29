# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Weather',
            fields=[
                (
                    'id',
                    models.AutoField(
                        verbose_name='ID', serialize=False, auto_created=True, primary_key=True
                    ),
                ),
                ('station_id', models.CharField(max_length=10)),
                ('timestamp', models.DateTimeField(unique=True, verbose_name=b'Date of reading')),
                ('wind_dir', models.IntegerField(null=True)),
                ('wind_speed', models.DecimalField(null=True, max_digits=5, decimal_places=2)),
                ('wind_peak', models.DecimalField(null=True, max_digits=5, decimal_places=2)),
                ('humidity', models.IntegerField(null=True)),
                ('temp', models.DecimalField(null=True, max_digits=5, decimal_places=2)),
                ('rain', models.DecimalField(null=True, max_digits=4, decimal_places=2)),
                ('barometer', models.DecimalField(null=True, max_digits=4, decimal_places=2)),
                ('dewpoint', models.DecimalField(null=True, max_digits=4, decimal_places=2)),
                ('temp_inside', models.DecimalField(null=True, max_digits=5, decimal_places=2)),
                ('baro_trend', models.DecimalField(null=True, max_digits=3, decimal_places=2)),
                ('windchill', models.DecimalField(null=True, max_digits=5, decimal_places=2)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
            bases=(models.Model,),
        ),
    ]
