# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-21 11:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='account',
            table='accounts',
        ),
    ]