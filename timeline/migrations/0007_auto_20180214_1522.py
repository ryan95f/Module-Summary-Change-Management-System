# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-14 15:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0006_tablechanges'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TableChanges',
            new_name='TableChange',
        ),
    ]
