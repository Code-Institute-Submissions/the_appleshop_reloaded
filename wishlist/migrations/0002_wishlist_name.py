# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-06-12 05:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='wishlist',
            name='name',
            field=models.CharField(default='', max_length=254),
        ),
    ]