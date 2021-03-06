# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-23 19:08
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0002_auto_20160822_2034'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='food',
            name='user',
        ),
        migrations.AddField(
            model_name='food',
            name='ingredients',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
        ),
        migrations.AddField(
            model_name='food',
            name='nutrients',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
        ),
        migrations.AddField(
            model_name='food',
            name='recipe_yield',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='food',
            name='servings',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
    ]
