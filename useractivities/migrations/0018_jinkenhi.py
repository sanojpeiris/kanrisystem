# Generated by Django 2.2.7 on 2019-12-19 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useractivities', '0017_auto_20191217_1544'),
    ]

    operations = [
        migrations.CreateModel(
            name='jinkenhi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('edit_username', models.TextField(null=True)),
                ('user_id', models.IntegerField(null=True)),
                ('username', models.TextField(null=True)),
                ('department', models.TextField(null=True)),
                ('product_id', models.IntegerField(null=True)),
                ('itemname', models.TextField(null=True)),
                ('kaigai', models.TextField(null=True)),
                ('percentage', models.IntegerField(null=True)),
                ('Date', models.DateField(auto_now_add=True, null=True)),
                ('created_month', models.CharField(max_length=100, null=True)),
                ('Month', models.CharField(max_length=100, null=True)),
                ('time', models.TimeField(auto_now_add=True)),
                ('done', models.BooleanField(default=False)),
                ('kakunin', models.BooleanField(default=False)),
            ],
        ),
    ]