# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-13 18:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Buses', '0003_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='CurrentLocation',
            fields=[
                ('license_plate', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('lattitude', models.CharField(max_length=20)),
                ('longitute', models.CharField(max_length=20)),
                ('passengers', models.IntegerField(verbose_name='Number of passengers')),
            ],
        ),
        migrations.RenameModel(
            old_name='Location',
            new_name='LocationHistory',
        ),
    ]
