# Generated by Django 3.2.14 on 2022-07-22 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0003_auto_20220722_0327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='length_seconds',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='publish_date',
            field=models.DateField(null=True),
        ),
    ]
