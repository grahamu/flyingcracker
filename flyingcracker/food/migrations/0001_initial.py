# -*- coding: utf-8 -*-
import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                (
                    'id',
                    models.AutoField(
                        verbose_name='ID', serialize=False, auto_created=True, primary_key=True
                    ),
                ),
                ('title', models.CharField(max_length=20)),
            ],
            options={
                'ordering': ['title'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                (
                    'id',
                    models.AutoField(
                        verbose_name='ID', serialize=False, auto_created=True, primary_key=True
                    ),
                ),
                ('title', models.CharField(max_length=20)),
                ('slug', models.SlugField()),
                ('description', models.TextField(null=True, blank=True)),
            ],
            options={
                'ordering': ['title'],
                'verbose_name_plural': 'categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Foodstuff',
            fields=[
                (
                    'id',
                    models.AutoField(
                        verbose_name='ID', serialize=False, auto_created=True, primary_key=True
                    ),
                ),
                ('title', models.CharField(unique=True, max_length=100)),
                ('description', models.TextField(null=True, blank=True)),
                ('slug', models.SlugField()),
            ],
            options={
                'ordering': ['title'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                (
                    'id',
                    models.AutoField(
                        verbose_name='ID', serialize=False, auto_created=True, primary_key=True
                    ),
                ),
                ('quantity', models.CharField(max_length=20, null=True, blank=True)),
                ('modifier', models.CharField(max_length=50, null=True, blank=True)),
                ('rank', models.IntegerField()),
                (
                    'foodstuff',
                    models.ForeignKey(
                        related_name='ingredients', to='food.Foodstuff', on_delete=models.CASCADE
                    ),
                ),
            ],
            options={
                'ordering': ['rank'],
                'verbose_name': 'recipe ingredient',
                'verbose_name_plural': 'recipe ingredients',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                (
                    'id',
                    models.AutoField(
                        verbose_name='ID', serialize=False, auto_created=True, primary_key=True
                    ),
                ),
                ('title', models.CharField(unique=True, max_length=50)),
                ('url', models.CharField(max_length=250)),
                ('rank', models.IntegerField()),
            ],
            options={
                'ordering': ['rank'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                (
                    'id',
                    models.AutoField(
                        verbose_name='ID', serialize=False, auto_created=True, primary_key=True
                    ),
                ),
                ('title', models.CharField(unique=True, max_length=50, db_index=True)),
                ('slug', models.SlugField()),
                (
                    'pub_date',
                    models.DateField(
                        default=datetime.date.today, null=True, verbose_name=b'date published'
                    ),
                ),
                ('directions', models.TextField(null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('teaser', models.CharField(max_length=100, null=True, blank=True)),
                ('credit', models.TextField(null=True, blank=True)),
                (
                    'rclass',
                    models.CharField(
                        default=b'D',
                        max_length=1,
                        choices=[(b'D', b'Drink'), (b'E', b'Eat'), (b'I', b'Ingredient')],
                    ),
                ),
                ('attributes', models.ManyToManyField(to='food.Attribute')),
                ('categories', models.ManyToManyField(to='food.Category')),
            ],
            options={
                'ordering': ['title'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='recipe',
            field=models.ForeignKey(related_name='ingredients', to='food.Recipe', on_delete=models.CASCADE),
            preserve_default=True,
        ),
    ]
