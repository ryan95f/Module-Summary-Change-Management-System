# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-14 15:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_merge_20180207_1713'),
        ('timeline', '0005_timelineentry_entry_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='TableChanges',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('changes_for', models.CharField(max_length=30)),
                ('changes_field', models.CharField(max_length=30)),
                ('current_value', models.CharField(max_length=50)),
                ('new_value', models.CharField(max_length=50)),
                ('related_entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timeline.TimelineEntry')),
                ('related_module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Module')),
            ],
        ),
    ]
