# Generated by Django 5.0.1 on 2024-02-07 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0010_alter_imagenhistoriaclinica_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagenhistoriaclinica',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='img_hc'),
        ),
    ]
