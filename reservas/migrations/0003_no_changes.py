# Migración vacía para evitar conflictos
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0002_alter_escritoriodedicado_posicion_x_and_more'),
    ]

    operations = [
        # No hacemos cambios - la base de datos ya está correcta
    ]
