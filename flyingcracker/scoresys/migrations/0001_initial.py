# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ResultPoints',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('result', models.CharField(max_length=50)),
                ('points', models.IntegerField()),
                ('rank', models.PositiveIntegerField(default=1)),
            ],
            options={
                'ordering': ['rank'],
                'verbose_name_plural': 'Result points',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ScoringSystem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name=b'Scoring system name')),
                ('num_places', models.PositiveIntegerField()),
                ('description', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='resultpoints',
            name='system',
            field=models.ForeignKey(to='scoresys.ScoringSystem'),
            preserve_default=True,
        ),
    ]
