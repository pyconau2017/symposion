# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-10 06:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('symposion_schedule', '0004_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slot',
            name='name',
            field=models.CharField(editable=False, max_length=512),
        ),
    ]
