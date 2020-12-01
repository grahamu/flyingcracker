# -*- coding: utf-8 -*-
from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='ChartUrl',
            fields=[
                (
                    'id',
                    models.AutoField(
                        verbose_name='ID', serialize=False, auto_created=True, primary_key=True
                    ),
                ),
                ('date', models.DateField()),
                ('timestamp', models.DateTimeField(default=datetime.datetime.now)),
                ('data_type', models.CharField(max_length=2)),
                ('unit', models.CharField(max_length=5)),
                ('size', models.CharField(max_length=2)),
                ('plots', models.CharField(max_length=10)),
                ('url', models.URLField(max_length=2000)),
            ],
            options={
                'ordering': ['-date'],
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='charturl',
            unique_together=set([('date', 'data_type', 'unit', 'size', 'plots')]),
        ),
    ]
