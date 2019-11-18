# Generated by Django 2.2.5 on 2019-11-15 09:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('useractivities', '0004_taskmessage_visible'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskmessage',
            name='spec_user',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='taskmessage',
            name='edit_username',
            field=models.TextField(null=True),
        ),
    ]