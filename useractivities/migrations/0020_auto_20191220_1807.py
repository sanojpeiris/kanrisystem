# Generated by Django 2.2.7 on 2019-12-20 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useractivities', '0019_remove_jinkenhi_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jinkenhi',
            name='Month',
            field=models.CharField(max_length=99, null=True),
        ),
    ]
