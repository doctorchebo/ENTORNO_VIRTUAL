# Generated by Django 3.2.5 on 2022-02-28 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custodia', '0025_auto_20220227_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='desembolsos',
            name='fecha_creacion',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='desembolsos',
            name='fecha_modificacion',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
