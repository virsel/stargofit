# Generated by Django 2.2 on 2019-08-22 06:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('training_plans', '0062_auto_20190822_0717'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cooldown',
            name='time',
        ),
        migrations.RemoveField(
            model_name='set',
            name='time',
        ),
        migrations.RemoveField(
            model_name='training',
            name='time',
        ),
        migrations.RemoveField(
            model_name='warmup',
            name='time',
        ),
        migrations.RemoveField(
            model_name='workout',
            name='time',
        ),
    ]
