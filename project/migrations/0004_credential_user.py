# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-10 23:26
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_auto_20170311_0721'),
    ]

    operations = [
        migrations.AddField(
            model_name='credential',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
