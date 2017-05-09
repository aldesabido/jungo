# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-12 00:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0020_auto_20170312_0816'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='company',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='project.Company'),
            preserve_default=False,
        ),
    ]
