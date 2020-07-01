# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-06-18 23:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product_use'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='fruit',
            field=models.CharField(choices=[('apple', 'apple'), ('pear', 'pear')], default='', max_length=254),
        ),
    ]
