# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-03-26 09:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('symposion_schedule', '0008_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slot',
            name='name',
            field=models.CharField(editable=False, max_length=512),
        ),
    ]
