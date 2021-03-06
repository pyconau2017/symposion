# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-17 03:35
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('symposion_proposals', '__first__'),
        ('symposion_speakers', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('symposion_conference', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Date')),
            ],
            options={
                'ordering': ['date'],
                'verbose_name': 'date',
                'verbose_name_plural': 'dates',
            },
        ),
        migrations.CreateModel(
            name='Presentation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('abstract', models.TextField(verbose_name='Abstract')),
                ('abstract_html', models.TextField(blank=True)),
                ('cancelled', models.BooleanField(default=False, verbose_name='Cancelled')),
                ('additional_speakers', models.ManyToManyField(blank=True, related_name='copresentations', to='symposion_speakers.Speaker', verbose_name='Additional speakers')),
                ('proposal_base', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='presentation', to='symposion_proposals.ProposalBase', verbose_name='Proposal base')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='presentations', to='symposion_conference.Section', verbose_name='Section')),
            ],
            options={
                'ordering': ['slot'],
                'verbose_name': 'presentation',
                'verbose_name_plural': 'presentations',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=65, verbose_name='Name')),
                ('order', models.PositiveIntegerField(verbose_name='Order')),
            ],
            options={
                'verbose_name': 'Room',
                'verbose_name_plural': 'Rooms',
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('published', models.BooleanField(default=True, verbose_name='Published')),
                ('hidden', models.BooleanField(default=False, verbose_name='Hide schedule from overall conference view')),
                ('section', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='symposion_conference.Section', verbose_name='Section')),
            ],
            options={
                'ordering': ['section'],
                'verbose_name': 'Schedule',
                'verbose_name_plural': 'Schedules',
            },
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to='symposion_schedule.Day', verbose_name='Day')),
            ],
            options={
                'verbose_name': 'Session',
                'verbose_name_plural': 'Sessions',
            },
        ),
        migrations.CreateModel(
            name='SessionRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.IntegerField(choices=[(1, 'Session Chair'), (2, 'Session Runner')], verbose_name='Role')),
                ('status', models.NullBooleanField(verbose_name='Status')),
                ('submitted', models.DateTimeField(default=datetime.datetime.now)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='symposion_schedule.Session', verbose_name='Session')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Session role',
                'verbose_name_plural': 'Session roles',
            },
        ),
        migrations.CreateModel(
            name='Slot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(editable=False, max_length=100)),
                ('start', models.TimeField(verbose_name='Start')),
                ('end', models.TimeField(verbose_name='End')),
                ('content_override', models.TextField(blank=True, verbose_name='Content override')),
                ('content_override_html', models.TextField(blank=True)),
                ('day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='symposion_schedule.Day', verbose_name='Day')),
            ],
            options={
                'ordering': ['day', 'start', 'end'],
                'verbose_name': 'slot',
                'verbose_name_plural': 'slots',
            },
        ),
        migrations.CreateModel(
            name='SlotKind',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=50, verbose_name='Label')),
                ('schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='symposion_schedule.Schedule', verbose_name='schedule')),
            ],
            options={
                'verbose_name': 'Slot kind',
                'verbose_name_plural': 'Slot kinds',
            },
        ),
        migrations.CreateModel(
            name='SlotRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='symposion_schedule.Room', verbose_name='Room')),
                ('slot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='symposion_schedule.Slot', verbose_name='Slot')),
            ],
            options={
                'ordering': ['slot', 'room__order'],
                'verbose_name': 'Slot room',
                'verbose_name_plural': 'Slot rooms',
            },
        ),
        migrations.AddField(
            model_name='slot',
            name='kind',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='symposion_schedule.SlotKind', verbose_name='Kind'),
        ),
        migrations.AddField(
            model_name='session',
            name='slots',
            field=models.ManyToManyField(related_name='sessions', to='symposion_schedule.Slot', verbose_name='Slots'),
        ),
        migrations.AddField(
            model_name='room',
            name='schedule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='symposion_schedule.Schedule', verbose_name='Schedule'),
        ),
        migrations.AddField(
            model_name='presentation',
            name='slot',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='content_ptr', to='symposion_schedule.Slot', verbose_name='Slot'),
        ),
        migrations.AddField(
            model_name='presentation',
            name='speaker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='presentations', to='symposion_speakers.Speaker', verbose_name='Speaker'),
        ),
        migrations.AddField(
            model_name='day',
            name='schedule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='symposion_schedule.Schedule', verbose_name='Schedule'),
        ),
        migrations.AlterUniqueTogether(
            name='slotroom',
            unique_together=set([('slot', 'room')]),
        ),
        migrations.AlterUniqueTogether(
            name='sessionrole',
            unique_together=set([('session', 'user', 'role')]),
        ),
        migrations.AlterUniqueTogether(
            name='day',
            unique_together=set([('schedule', 'date')]),
        ),
    ]
