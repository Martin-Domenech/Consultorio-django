# Generated by Django 5.0.1 on 2024-01-31 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0004_remove_historiaclinica_fecha_um_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historiaclinica',
            name='fecha',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
