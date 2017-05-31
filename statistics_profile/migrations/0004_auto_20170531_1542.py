# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-31 15:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20170531_1542'),
        ('statistics_profile', '0003_remove_statistics_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='statistics',
            name='comments',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='statistics',
            name='count_images',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='statistics',
            name='count_media',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='statistics',
            name='count_videos',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='statistics',
            name='followed_by',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='statistics',
            name='follows',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='statistics',
            name='follows_change',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='statistics',
            name='involvement',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=6),
        ),
        migrations.AddField(
            model_name='statistics',
            name='likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='statistics',
            name='likes_average',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
        migrations.AddField(
            model_name='statistics',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='accounts.Profile'),
        ),
    ]
