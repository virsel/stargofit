# Generated by Django 2.2 on 2019-07-10 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training_plans', '0012_auto_20190710_0244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='training_plan',
            name='title',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
