# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-10-18 19:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('belt_exam_app', '0003_auto_20191018_1945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='likeCount',
            field=models.IntegerField(default=False),
        ),
    ]
