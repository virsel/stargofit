# Generated by Django 2.2 on 2019-11-24 10:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('training_plans', '0088_currentplan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currentplan',
            name='member',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='current_plan', to=settings.AUTH_USER_MODEL),
        ),
    ]
