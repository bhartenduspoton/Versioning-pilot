# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comments', models.CharField(max_length=1000, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Phase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phase', models.CharField(max_length=1000, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('customerID', models.IntegerField(default=1)),
                ('projectID', models.IntegerField(default=1)),
                ('projectName', models.CharField(default=b'default', max_length=200)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TotalG',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phase', models.IntegerField(max_length=1000, null=True, blank=True)),
                ('TG1', models.CharField(max_length=1000, null=True, blank=True)),
                ('TG2', models.CharField(max_length=1000, null=True, blank=True)),
                ('TG3', models.CharField(max_length=1000, null=True, blank=True)),
                ('TG4', models.CharField(max_length=1000, null=True, blank=True)),
                ('project', models.ForeignKey(to='main.Project')),
            ],
        ),
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('docfile', models.FileField(upload_to=b'documents/')),
            ],
        ),
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('version', models.IntegerField(default=1, null=True, blank=True)),
                ('file_path', models.CharField(max_length=200, null=True, blank=True)),
                ('processed', models.BooleanField(default=False)),
                ('excelsheet', models.FileField(upload_to=b'documents/')),
                ('file_name', models.CharField(max_length=200, null=True, blank=True)),
                ('comments', models.CharField(max_length=1000, null=True, blank=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('project', models.ForeignKey(to='main.Project')),
            ],
        ),
        migrations.AddField(
            model_name='phase',
            name='project',
            field=models.ForeignKey(to='main.Project'),
        ),
        migrations.AddField(
            model_name='comment',
            name='UserData',
            field=models.ForeignKey(to='main.UserData'),
        ),
    ]
