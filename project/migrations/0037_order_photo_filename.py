# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-09 07:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0036_remove_order_photo_is_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_photo',
            name='filename',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
