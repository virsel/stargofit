# Generated by Django 2.2 on 2020-01-05 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training_plans', '0108_auto_20200105_1925'),
    ]

    operations = [
        migrations.AddField(
            model_name='musclegroup',
            name='title_de',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='musclegroup',
            name='title_en',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
