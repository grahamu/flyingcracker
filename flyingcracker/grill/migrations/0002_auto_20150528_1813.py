# -*- coding: utf-8 -*-
from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('grill', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grilling',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
