# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-24 08:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0017_remove_post_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
