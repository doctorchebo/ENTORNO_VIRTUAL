# Generated by Django 3.2.5 on 2022-02-21 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custodia', '0010_alter_apertura_codigo_cliente'),
    ]

    operations = [
        migrations.AddField(
            model_name='poliza',
            name='bloque',
            field=models.PositiveBigIntegerField(null=True),
        ),
    ]
