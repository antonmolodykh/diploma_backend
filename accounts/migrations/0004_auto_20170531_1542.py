# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-31 15:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20170521_1147'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Account',
            new_name='Profile',
        ),
    ]
