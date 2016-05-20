# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-19 23:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='camera',
            name='site',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='observations.Site'),
        ),
        migrations.AlterField(
            model_name='penguincount',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='observations.Site'),
        ),
        migrations.AlterField(
            model_name='penguinobservation',
            name='camera',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='observations.Camera'),
        ),
        migrations.AlterField(
            model_name='penguinobservation',
            name='observer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='observations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='penguinobservation',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='observations.Site'),
        ),
        migrations.AlterField(
            model_name='penguinobservation',
            name='video',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='observations.Video', verbose_name='Video filename'),
        ),
        migrations.AlterField(
            model_name='penguinvideoobservation',
            name='video',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='observations.Video'),
        ),
        migrations.AlterField(
            model_name='video',
            name='camera',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='observations.Camera'),
        ),
    ]
