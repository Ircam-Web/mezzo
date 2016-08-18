# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-18 10:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization-magazine', '0019_auto_20160818_1233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brief',
            name='external_content',
            field=models.URLField(blank=True, max_length=1000, verbose_name='external content'),
        ),
        migrations.AlterField(
            model_name='brief',
            name='external_content_en',
            field=models.URLField(blank=True, max_length=1000, null=True, verbose_name='external content'),
        ),
        migrations.AlterField(
            model_name='brief',
            name='external_content_fr',
            field=models.URLField(blank=True, max_length=1000, null=True, verbose_name='external content'),
        ),
    ]
