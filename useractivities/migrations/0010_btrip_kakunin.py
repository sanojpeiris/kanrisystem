# Generated by Django 2.2.7 on 2019-11-28 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useractivities', '0009_auto_20191127_1346'),
    ]

    operations = [
        migrations.AddField(
            model_name='btrip',
            name='kakunin',
            field=models.BooleanField(default=False),
        ),
    ]
