# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-17 03:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import timezone_field.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Conference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='Start date')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='End date')),
                ('timezone', timezone_field.fields.TimeZoneField(blank=True, verbose_name='timezone')),
            ],
            options={
                'verbose_name': 'conference',
                'verbose_name_plural': 'conferences',
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('slug', models.SlugField(verbose_name='Slug')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='Start date')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='End date')),
                ('conference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='symposion_conference.Conference', verbose_name='Conference')),
            ],
            options={
                'ordering': ['start_date'],
                'verbose_name': 'section',
                'verbose_name_plural': 'sections',
            },
        ),
    ]
