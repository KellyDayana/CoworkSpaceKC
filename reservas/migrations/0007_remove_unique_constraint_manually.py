# Generated manually to fix unique_together constraint issue
from django.db import migrations


def remove_all_unique_constraints(apps, schema_editor):
    """
    Elimina todos los constraints únicos relacionados con piso/posicion
    en la tabla reservas_escritoriodedicado
    """
    if schema_editor.connection.vendor == 'postgresql':
        with schema_editor.connection.cursor() as cursor:
            # Buscar todos los constraints únicos en la tabla
            cursor.execute("""
                SELECT conname 
                FROM pg_constraint 
                WHERE conrelid = 'reservas_escritoriodedicado'::regclass 
                AND contype = 'u'
                AND (
                    conname LIKE '%posicion%' 
                    OR conname LIKE '%piso%'
                );
            """)
            
            constraints = cursor.fetchall()
            
            # Eliminar cada constraint encontrado
            for (constraint_name,) in constraints:
                cursor.execute(f'ALTER TABLE reservas_escritoriodedicado DROP CONSTRAINT IF EXISTS {constraint_name};')


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0006_alter_escritoriodedicado_options_and_more'),
    ]

    operations = [
        migrations.RunPython(
            remove_all_unique_constraints,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
