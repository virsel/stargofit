# Generated by Django 2.2 on 2019-12-24 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training_plans', '0089_auto_20191124_1157'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area', models.CharField(blank=True, max_length=40, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/exercise_kinds/')),
                ('identify', models.CharField(blank=True, max_length=40, null=True)),
            ],
        ),
    ]
