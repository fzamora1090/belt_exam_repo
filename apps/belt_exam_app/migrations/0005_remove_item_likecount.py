# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-10-18 19:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('belt_exam_app', '0004_auto_20191018_1948'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='likeCount',
        ),
    ]