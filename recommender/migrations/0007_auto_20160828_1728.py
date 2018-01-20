# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-28 15:28
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recommender', '0006_auto_20160828_1620'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_history', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=[])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='eater',
            name='user',
        ),
        migrations.DeleteModel(
            name='Eater',
        ),
    ]