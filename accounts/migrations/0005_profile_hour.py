# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-01 13:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20170531_1542'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='hour',
            field=models.IntegerField(null=True),
        ),
    ]
