# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-06 16:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import mezzanine.core.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pages', '0004_auto_20151223_1313'),
    ]

    operations = [
        migrations.CreateModel(
            name='BasicPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pages.Page')),
                ('content', mezzanine.core.fields.RichTextField(verbose_name='Content')),
                ('photo', mezzanine.core.fields.FileField(blank=True, max_length=1024, verbose_name='photo')),
                ('photo_credits', models.CharField(blank=True, max_length=255, null=True, verbose_name='photo credits')),
                ('photo_alignment', models.CharField(blank=True, choices=[('left', 'left'), ('center', 'center'), ('right', 'right')], default='left', max_length=32, verbose_name='photo alignment')),
                ('photo_description', models.TextField(blank=True, verbose_name='photo description')),
                ('photo_card', mezzanine.core.fields.FileField(blank=True, max_length=1024, verbose_name='card photo')),
                ('photo_card_credits', models.CharField(blank=True, max_length=255, null=True, verbose_name='photo card credits')),
                ('photo_slider', mezzanine.core.fields.FileField(blank=True, max_length=1024, verbose_name='slider photo')),
                ('photo_slider_credits', models.CharField(blank=True, max_length=255, null=True, verbose_name='photo slider credits')),
                ('sub_title', models.TextField(blank=True, max_length=1024, verbose_name='sub title')),
                ('sub_title_fr', models.TextField(blank=True, max_length=1024, null=True, verbose_name='sub title')),
                ('sub_title_en', models.TextField(blank=True, max_length=1024, null=True, verbose_name='sub title')),
            ],
            options={
                'verbose_name': 'basic page',
                'ordering': ('_order',),
            },
            bases=('pages.page', models.Model),
        ),
    ]
