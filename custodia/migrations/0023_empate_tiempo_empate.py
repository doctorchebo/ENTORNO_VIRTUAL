# Generated by Django 3.2.5 on 2022-02-25 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custodia', '0022_alter_prestamo_sobre'),
    ]

    operations = [
        migrations.AddField(
            model_name='empate',
            name='tiempo_empate',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
