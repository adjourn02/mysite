# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-19 15:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0008_image_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='item',
            field=models.CharField(blank=True, max_length=11),
        ),
    ]
