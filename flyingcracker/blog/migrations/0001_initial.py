# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField(help_text=b'Automatically built from the title.')),
                ('teaser', models.TextField()),
                ('pub_date', models.DateTimeField(verbose_name=b'Date this post will get published')),
                ('body', models.TextField()),
                ('enable_comments', models.BooleanField(default=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-pub_date',),
                'get_latest_by': 'pub_date',
            },
            bases=(models.Model,),
        ),
    ]
