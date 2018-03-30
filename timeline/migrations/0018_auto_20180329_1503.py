# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-29 14:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0017_timelineentry_parent_entry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timelineentry',
            name='content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
        migrations.AlterField(
            model_name='timelineentry',
            name='object_id',
            field=models.CharField(default=0, max_length=10),
        ),
    ]
