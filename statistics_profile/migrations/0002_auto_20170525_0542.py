# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-25 05:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('statistics_profile', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='statistics',
            name='Involvement',
        ),
        migrations.RemoveField(
            model_name='statistics',
            name='account',
        ),
        migrations.RemoveField(
            model_name='statistics',
            name='comments',
        ),
        migrations.RemoveField(
            model_name='statistics',
            name='count_images',
        ),
        migrations.RemoveField(
            model_name='statistics',
            name='count_media',
        ),
        migrations.RemoveField(
            model_name='statistics',
            name='count_videos',
        ),
        migrations.RemoveField(
            model_name='statistics',
            name='followed_by',
        ),
        migrations.RemoveField(
            model_name='statistics',
            name='follows',
        ),
        migrations.RemoveField(
            model_name='statistics',
            name='likes_average',
        ),
    ]
