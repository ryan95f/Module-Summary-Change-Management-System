# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-11 19:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0002_auto_20180208_1643'),
    ]

    operations = [
        migrations.AddField(
            model_name='timelineentry',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='timelineentry',
            name='status',
            field=models.CharField(choices=[('Draft', 'Draft'), ('Staged', 'Staged'), ('Confirmed', 'Confirmed')], default='Draft', max_length=9),
        ),
    ]