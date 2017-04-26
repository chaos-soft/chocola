# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-26 18:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('md5', models.CharField(max_length=32)),
                ('file', models.FileField(max_length=255, upload_to='files/%Y/%m')),
                ('size', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='files.File')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.AlterIndexTogether(
            name='file',
            index_together=set([('md5', 'size')]),
        ),
    ]
