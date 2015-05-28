# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0002_auto_20150528_0457'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalProject',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('customerID', models.IntegerField(default=1)),
                ('projectID', models.IntegerField(default=1)),
                ('projectName', models.CharField(default=b'default', max_length=200)),
                ('date', models.DateTimeField(editable=False, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical project',
            },
        ),
        migrations.CreateModel(
            name='HistoricalTotalG',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('phase', models.IntegerField(null=True, blank=True)),
                ('TG1', models.CharField(max_length=1000, null=True, blank=True)),
                ('TG2', models.CharField(max_length=1000, null=True, blank=True)),
                ('TG3', models.CharField(max_length=1000, null=True, blank=True)),
                ('TG4', models.CharField(max_length=1000, null=True, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('project', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='main.Project', null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical total g',
            },
        ),
        migrations.CreateModel(
            name='HistoricalUserData',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('version', models.IntegerField(default=1, null=True, blank=True)),
                ('file_path', models.CharField(max_length=200, null=True, blank=True)),
                ('processed', models.BooleanField(default=False)),
                ('excelsheet', models.TextField(max_length=100)),
                ('file_name', models.CharField(max_length=200, null=True, blank=True)),
                ('comments', models.CharField(max_length=1000, null=True, blank=True)),
                ('created_on', models.DateTimeField(editable=False, blank=True)),
                ('updated_on', models.DateTimeField(editable=False, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('project', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='main.Project', null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical user data',
            },
        ),
    ]
