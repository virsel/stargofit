# Generated by Django 2.2 on 2019-10-18 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training_plans', '0084_training_plan_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='training',
            name='kind',
            field=models.CharField(blank=True, choices=[('0', 'Muskelaufbau'), ('1', 'Kraftaufbau'), ('2', 'Definition'), ('3', 'Ausdauer'), ('4', 'Fettverbrennung'), ('5', 'Beweglichkeit')], max_length=70, null=True),
        ),
    ]
