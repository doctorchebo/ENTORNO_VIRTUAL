# Generated by Django 3.2.5 on 2022-02-28 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custodia', '0028_delete_tipogarantia'),
    ]

    operations = [
        migrations.AddField(
            model_name='correspondencia',
            name='documento_suelto',
            field=models.ManyToManyField(blank=True, to='custodia.DocumentosSueltos'),
        ),
    ]
