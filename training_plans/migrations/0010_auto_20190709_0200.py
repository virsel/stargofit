# Generated by Django 2.2 on 2019-07-09 00:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('training_plans', '0009_auto_20190708_2344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eendurancetraining',
            name='exercise_ptr',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='endurance', serialize=False, to='training_plans.Exercise'),
        ),
    ]
