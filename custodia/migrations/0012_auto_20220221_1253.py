# Generated by Django 3.2.5 on 2022-02-21 16:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("custodia", "0011_poliza_bloque"),
    ]

    operations = [
        migrations.AlterField(
            model_name="documentossueltos",
            name="bloque",
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="documentossueltos",
            name="caja",
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="documentossueltos",
            name="fecha_creacion",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name="documentossueltos",
            name="fecha_modificacion",
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name="documentossueltos",
            name="usuario_creacion",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="usuario_creacion_documento_suelto",
                to="custodia.profile",
            ),
        ),
        migrations.AlterField(
            model_name="documentossueltos",
            name="usuario_modificacion",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="usuario_modificacion_documento_suelto",
                to="custodia.profile",
            ),
        ),
    ]
