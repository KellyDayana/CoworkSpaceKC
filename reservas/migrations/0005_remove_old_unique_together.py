# Generated migration to remove problematic unique_together

from django.db import migrations


def remove_old_constraints(apps, schema_editor):
    """
    Elimina constraints antiguos si existen.
    Si las columnas ya no existen, ignora el error.
    """
    if schema_editor.connection.vendor == 'postgresql':
        with schema_editor.connection.cursor() as cursor:
            # Intentar eliminar constraints antiguos con posicion_x/posicion_y
            try:
                cursor.execute("""
                    SELECT conname 
                    FROM pg_constraint 
                    WHERE conrelid = 'reservas_escritoriodedicado'::regclass 
                    AND contype = 'u';
                """)
                
                constraints = cursor.fetchall()
                
                for (constraint_name,) in constraints:
                    try:
                        cursor.execute(f'ALTER TABLE reservas_escritoriodedicado DROP CONSTRAINT IF EXISTS {constraint_name};')
                    except Exception:
                        # Ignorar errores si el constraint no se puede eliminar
                        pass
            except Exception:
                # Si la tabla no existe o hay otro error, continuar
                pass


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0004_alter_escritoriodedicado_options_and_more'),
    ]

    operations = [
        migrations.RunPython(
            remove_old_constraints,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
