# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-22 18:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('id_string', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=200)),
                ('url', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('join_date', models.DateTimeField(verbose_name='Date joined')),
            ],
        ),
        migrations.AddField(
            model_name='food',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recommender.User'),
        ),
    ]
