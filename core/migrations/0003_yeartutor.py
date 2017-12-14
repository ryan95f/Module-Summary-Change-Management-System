# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-14 13:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20171214_1242'),
    ]

    operations = [
        migrations.CreateModel(
            name='YearTutor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tutor_year', models.CharField(choices=[('year 1', 'Year 1'), ('year 2', 'Year 2'), ('year 3', 'Year 3'), ('msc', 'MSC')], default='year 1', max_length=7)),
                ('year_tutor_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]