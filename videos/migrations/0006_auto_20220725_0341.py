# Generated by Django 3.2.14 on 2022-07-25 03:41

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0005_titleinvertedindex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='titleinvertedindex',
            name='videosId',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), blank=True, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='titleinvertedindex',
            name='videosTitle',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), blank=True, null=True, size=None),
        ),
    ]
