# Generated by Django 2.2.7 on 2019-11-22 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useractivities', '0004_auto_20191122_1804'),
    ]

    operations = [
        migrations.AddField(
            model_name='kintai',
            name='result',
            field=models.TextField(null=True),
        ),
    ]
