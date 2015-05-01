# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
        ('scoresys', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Competitor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('active', models.BooleanField(default=True, help_text=b'Players may only pick "active" competitors.')),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('short_name', models.CharField(max_length=20, blank=True)),
                ('description', models.CharField(max_length=100, null=True, blank=True)),
                ('guess_deadline', models.DateTimeField(help_text=b'(format: YYYY-MM-DD HH:MM) in UTC (Greenwich time)', null=True, verbose_name=b'Guess cutoff date & time', blank=True)),
                ('start', models.DateTimeField(help_text=b'(format: YYYY-MM-DD HH:MM) in UTC (Greenwich time)', verbose_name=b'Event start date & time')),
                ('location', models.CharField(max_length=100, null=True, blank=True)),
                ('result_locked', models.BooleanField(default=False, help_text=b'If unlocked, users are allowed to enter results.', verbose_name=b'Lock results')),
            ],
            options={
                'ordering': ['start'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Guess',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('late_entry', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField()),
                ('competitor', models.ForeignKey(to='fantasy.Competitor')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'guesses',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('result', models.CharField(max_length=50)),
                ('competitor', models.ForeignKey(to='fantasy.Competitor')),
                ('entered_by', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('event', models.ForeignKey(to='fantasy.Event')),
            ],
            options={
                'ordering': ['result'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('description', models.CharField(max_length=100, null=True, blank=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('competitor_label', models.CharField(default=b'Driver', help_text=b'How competitors are referred to, i.e. "Driver" or "Rider".', max_length=50)),
                ('event_label', models.CharField(default=b'Race', help_text=b'How series events are referred to, i.e. "Race" or "Stage".', max_length=50)),
                ('num_guesses', models.PositiveIntegerField(default=1, help_text=b'The number of competitors a user can pick for each event.', verbose_name=b'# guesses')),
                ('guess_once_per_series', models.BooleanField(default=False, verbose_name=b'Pick competitors once for entire series')),
                ('allow_late_guesses', models.BooleanField(default=False, help_text=b'Late guesses will not count in Series standings', verbose_name=b'Allow late guesses')),
                ('late_entry_footnote', models.CharField(default=b'player entered late picks', max_length=100, blank=True)),
                ('invite_only', models.BooleanField(default=False, verbose_name=b'Users must be invited')),
                ('only_members_can_view', models.BooleanField(default=False, verbose_name=b'Only members can view results')),
                ('users_enter_competitors', models.BooleanField(default=True, verbose_name=b'Users can add competitors')),
                ('status', models.CharField(default=b'H', max_length=1, choices=[(b'H', b'HIDDEN - only admin can view'), (b'A', b'ACTIVE - ready for use'), (b'C', b'COMPLETE - series is finished')])),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('scoring_system', models.ForeignKey(blank=True, to='scoresys.ScoringSystem', null=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'series',
                'verbose_name_plural': 'series',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('short_name', models.CharField(max_length=50, blank=True)),
                ('series', models.ForeignKey(to='fantasy.Series')),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='result',
            unique_together=set([('competitor', 'event', 'result')]),
        ),
        migrations.AddField(
            model_name='event',
            name='series',
            field=models.ForeignKey(to='fantasy.Series'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='event',
            unique_together=set([('name', 'series')]),
        ),
        migrations.AddField(
            model_name='competitor',
            name='series',
            field=models.ForeignKey(to='fantasy.Series'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='competitor',
            name='team',
            field=models.ForeignKey(blank=True, to='fantasy.Team', null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='competitor',
            unique_together=set([('name', 'series')]),
        ),
    ]
