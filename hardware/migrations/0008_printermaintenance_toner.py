# Generated by Django 5.2 on 2025-04-28 20:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hardware', '0007_remove_inkstock_printer_inkstock_toner_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='printermaintenance',
            name='toner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='maintenance_records', to='hardware.inkstock', verbose_name='Toner'),
        ),
    ]
