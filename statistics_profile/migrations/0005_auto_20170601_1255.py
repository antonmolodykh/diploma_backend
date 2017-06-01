# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-01 12:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statistics_profile', '0004_auto_20170531_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statistics',
            name='comments',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='statistics',
            name='count_images',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='statistics',
            name='count_media',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='statistics',
            name='count_videos',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='statistics',
            name='followed_by',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='statistics',
            name='follows',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='statistics',
            name='follows_change',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='statistics',
            name='involvement',
            field=models.DecimalField(decimal_places=4, max_digits=6, null=True),
        ),
        migrations.AlterField(
            model_name='statistics',
            name='likes',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='statistics',
            name='likes_average',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True),
        ),
    ]
