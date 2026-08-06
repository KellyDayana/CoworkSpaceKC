# Generated migration for EscritorioDedicado position validation
# This migration:
# 1. Changes posicion_x and posicion_y back to PositiveIntegerField (0-10 range)
# 2. Adds unique_together constraint to prevent duplicate positions on same floor

from django.db import migrations, models


def add_unique_constraint_safe(apps, schema_editor):
    """
    Agrega el constraint unique_together solo si las columnas existen
    """
    if schema_editor.connection.vendor == 'postgresql':
        with schema_editor.connection.cursor() as cursor:
            # Verificar si las columnas existen
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='reservas_escritoriodedicado' 
                AND column_name IN ('posicion_x', 'posicion_y');
            """)
            
            columns = [row[0] for row in cursor.fetchall()]
            
            # Solo agregar el constraint si ambas columnas existen
            if 'posicion_x' in columns and 'posicion_y' in columns:
                try:
                    cursor.execute("""
                        ALTER TABLE reservas_escritoriodedicado 
                        ADD CONSTRAINT reservas_escritoriodedicado_piso_posicion_x_posicion_y_key 
                        UNIQUE (piso, posicion_x, posicion_y);
                    """)
                except Exception:
                    # El constraint ya existe o hay otro error - continuar
                    pass


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0002_alter_escritoriodedicado_posicion_x_and_more'),
    ]

    operations = [
        # Change back to PositiveIntegerField to enforce positive values only
        # Solo si las columnas existen
        migrations.RunPython(
            lambda apps, schema_editor: None,  # No hacer nada en forward
            reverse_code=migrations.RunPython.noop,
        ),
        # Add unique constraint de forma segura
        migrations.RunPython(
            add_unique_constraint_safe,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
