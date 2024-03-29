# Generated by Django 3.2.5 on 2022-03-04 13:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('custodia', '0031_formatocontrato'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contratos',
            name='estado_cert_desgravamen',
            field=models.ForeignKey(blank=True, max_length=50, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='custodia.formatocontrato'),
        ),
        migrations.AlterField(
            model_name='contratos',
            name='estado_cert_fundempresa',
            field=models.ForeignKey(blank=True, max_length=50, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='custodia.formatocontrato'),
        ),
        migrations.AlterField(
            model_name='contratos',
            name='estado_cert_gravamen',
            field=models.ForeignKey(blank=True, max_length=50, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='custodia.formatocontrato'),
        ),
        migrations.AlterField(
            model_name='contratos',
            name='estado_cert_tdr',
            field=models.ForeignKey(blank=True, max_length=50, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='custodia.formatocontrato'),
        ),
        migrations.AlterField(
            model_name='contratos',
            name='estado_contrato',
            field=models.ForeignKey(blank=True, max_length=50, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='custodia.formatocontrato'),
        ),
        migrations.AlterField(
            model_name='contratos',
            name='estado_folio',
            field=models.ForeignKey(blank=True, max_length=50, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='custodia.formatocontrato'),
        ),
        migrations.AlterField(
            model_name='contratos',
            name='estado_inf_rapido',
            field=models.ForeignKey(blank=True, max_length=50, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='custodia.formatocontrato'),
        ),
        migrations.AlterField(
            model_name='contratos',
            name='estado_minuta',
            field=models.ForeignKey(blank=True, max_length=50, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='custodia.formatocontrato'),
        ),
        migrations.AlterField(
            model_name='contratos',
            name='estado_rec_firmas',
            field=models.ForeignKey(blank=True, max_length=50, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='custodia.formatocontrato'),
        ),
        migrations.AlterField(
            model_name='contratos',
            name='estado_seguro_cesantia',
            field=models.ForeignKey(blank=True, max_length=50, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='custodia.formatocontrato'),
        ),
        migrations.AlterField(
            model_name='contratos',
            name='estado_seguro_dima',
            field=models.ForeignKey(blank=True, max_length=50, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='custodia.formatocontrato'),
        ),
        migrations.AlterField(
            model_name='contratos',
            name='estado_testimonio',
            field=models.ForeignKey(blank=True, max_length=50, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='custodia.formatocontrato'),
        ),
    ]
