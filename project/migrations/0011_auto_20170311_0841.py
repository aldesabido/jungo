# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-11 00:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0010_auto_20170311_0829'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_hold',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='is_submit',
            field=models.BooleanField(default=False),
        ),
    ]
