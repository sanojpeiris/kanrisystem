# Generated by Django 2.2.5 on 2019-10-14 06:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('useractivities', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TodoItem',
            new_name='TaskItem',
        ),
    ]
