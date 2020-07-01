# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-06-13 03:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist', '0003_wishlist_products'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlist',
            name='products',
        ),
        migrations.AddField(
            model_name='wishlist',
            name='product_list',
            field=models.TextField(default='', max_length=254),
        ),
    ]