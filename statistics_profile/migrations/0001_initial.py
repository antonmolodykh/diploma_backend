# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-25 05:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0003_auto_20170521_1147'),
    ]

    operations = [
        migrations.CreateModel(
            name='Statistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('likes', models.IntegerField()),
                ('likes_average', models.DecimalField(decimal_places=2, max_digits=8)),
                ('comments', models.IntegerField()),
                ('follows', models.IntegerField()),
                ('followed_by', models.IntegerField()),
                ('count_media', models.IntegerField()),
                ('count_images', models.IntegerField()),
                ('count_videos', models.IntegerField()),
                ('Involvement', models.DecimalField(decimal_places=4, max_digits=6)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='accounts.Profile')),
            ],
            options={
                'db_table': 'statistics',
            },
        ),
    ]
