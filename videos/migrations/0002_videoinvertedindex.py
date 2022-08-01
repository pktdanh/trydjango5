# Generated by Django 3.2.14 on 2022-07-21 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoInvertedIndex',
            fields=[
                ('keyword', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('videos', models.ManyToManyField(related_name='keyword_in_videos', to='videos.Video')),
            ],
        ),
    ]
