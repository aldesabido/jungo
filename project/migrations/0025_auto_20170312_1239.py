# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-12 04:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0024_auto_20170312_1232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_status_history',
            name='status',
            field=models.CharField(max_length=200),
        ),
    ]
