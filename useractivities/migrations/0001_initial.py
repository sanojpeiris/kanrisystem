# Generated by Django 2.2.7 on 2019-11-22 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='kintai',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('edit_username', models.TextField(null=True)),
                ('type', models.TextField(null=True)),
                ('teiji', models.TextField(null=True)),
                ('ontime', models.TextField(null=True)),
                ('Date', models.DateField(null=True)),
                ('Month', models.CharField(max_length=100, null=True)),
                ('time', models.TimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TaskMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('edit_username', models.TextField(null=True)),
                ('spec_user', models.TextField()),
                ('message', models.TextField()),
                ('visible', models.BooleanField(default=True)),
                ('notification', models.BooleanField(default=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('time', models.TimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TaskTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('edit_username', models.TextField()),
                ('taskProject', models.TextField()),
                ('tasktype', models.TextField()),
                ('task', models.TextField()),
                ('date', models.DateField(auto_now_add=True)),
                ('time', models.TimeField(auto_now_add=True)),
            ],
        ),
    ]
