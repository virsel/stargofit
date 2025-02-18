# Generated by Django 2.2 on 2019-07-04 14:09

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('training_plans', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='instruction',
            name='step_de',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='instruction',
            name='step_en',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tipps',
            name='tipp_de',
            field=models.TextField(blank=True, max_length=70, null=True),
        ),
        migrations.AddField(
            model_name='tipps',
            name='tipp_en',
            field=models.TextField(blank=True, max_length=70, null=True),
        ),
        migrations.AlterField(
            model_name='emusclebuilding',
            name='muscle',
            field=models.CharField(blank=True, choices=[('vordere_schulter', 'vordere Schulter'), ('hintere_schulter', 'hintere Schulter'), ('seitliche_schulter', 'seitliche Schulter'), ('bizeps', 'Bizeps'), ('unterarme', 'Unterarme'), ('trizeps', 'Trizeps'), ('obere_brust', 'obere Brust'), ('mittlere_brust', 'mittlere Brust'), ('untere_brust', 'untere Brust'), ('seitlicher_bauch', 'seitlicher Bauch'), ('mittlere_bauch', 'mittlerer Bauch'), ('adduktoren', 'Adduktoren'), ('oberschenkel', 'Oberschenkel'), ('schienbein', 'Schienbein'), ('beinbizeps', 'Beinbizeps'), ('wade', 'Wade'), ('nacken', 'Nacken'), ('untergrätenmuskel', 'Untergrätenmuskel'), ('kapuzenmuskel', 'Kapuzenmuskel'), ('rautenmuskel', 'Rautenmuskel'), ('rundmuskel', 'Rundmuskel'), ('latissimus', 'Latissimus'), ('unterer_rücken', 'unterer Rücken'), ('po', 'Po')], default='bizeps', max_length=200),
        ),
        migrations.RemoveField(
            model_name='emusclebuilding',
            name='sub_muscles',
        ),
        migrations.AddField(
            model_name='emusclebuilding',
            name='sub_muscles',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('vordere_schulter', 'vordere Schulter'), ('hintere_schulter', 'hintere Schulter'), ('seitliche_schulter', 'seitliche Schulter'), ('bizeps', 'Bizeps'), ('unterarme', 'Unterarme'), ('trizeps', 'Trizeps'), ('obere_brust', 'obere Brust'), ('mittlere_brust', 'mittlere Brust'), ('untere_brust', 'untere Brust'), ('seitlicher_bauch', 'seitlicher Bauch'), ('mittlere_bauch', 'mittlerer Bauch'), ('adduktoren', 'Adduktoren'), ('oberschenkel', 'Oberschenkel'), ('schienbein', 'Schienbein'), ('beinbizeps', 'Beinbizeps'), ('wade', 'Wade'), ('nacken', 'Nacken'), ('untergrätenmuskel', 'Untergrätenmuskel'), ('kapuzenmuskel', 'Kapuzenmuskel'), ('rautenmuskel', 'Rautenmuskel'), ('rundmuskel', 'Rundmuskel'), ('latissimus', 'Latissimus'), ('unterer_rücken', 'unterer Rücken'), ('po', 'Po')], max_length=292, null=True),
        ),
    ]
