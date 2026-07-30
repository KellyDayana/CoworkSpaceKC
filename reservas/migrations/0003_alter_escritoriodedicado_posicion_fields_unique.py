# Generated migration for EscritorioDedicado position validation
# This migration:
# 1. Changes posicion_x and posicion_y back to PositiveIntegerField (0-10 range)
# 2. Adds unique_together constraint to prevent duplicate positions on same floor

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0002_alter_escritoriodedicado_posicion_x_and_more'),
    ]

    operations = [
        # Change back to PositiveIntegerField to enforce positive values only
        migrations.AlterField(
            model_name='escritoriodedicado',
            name='posicion_x',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='escritoriodedicado',
            name='posicion_y',
            field=models.PositiveIntegerField(default=0),
        ),
        # Add unique constraint to prevent duplicate positions on the same floor
        migrations.AlterUniqueTogether(
            name='escritoriodedicado',
            unique_together={('piso', 'posicion_x', 'posicion_y')},
        ),
    ]
