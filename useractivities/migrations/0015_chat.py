# Generated by Django 2.2.7 on 2019-12-13 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useractivities', '0014_auto_20191205_1657'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat', models.TextField(null=True)),
            ],
        ),
    ]