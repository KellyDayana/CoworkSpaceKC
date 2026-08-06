# Generated manually to fix unique_together constraint issue
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0006_alter_escritoriodedicado_options_and_more'),
    ]

    operations = [
        # Eliminar manualmente el constraint unique_together que causa problemas
        migrations.RunSQL(
            sql="""
                DO $$ 
                BEGIN
                    -- Intentar eliminar el constraint si existe
                    IF EXISTS (
                        SELECT 1 FROM pg_constraint 
                        WHERE conname = 'reservas_escritoriodedicado_piso_posicion_key'
                    ) THEN
                        ALTER TABLE reservas_escritoriodedicado 
                        DROP CONSTRAINT reservas_escritoriodedicado_piso_posicion_key;
                    END IF;
                    
                    -- También intentar eliminar variantes del nombre
                    IF EXISTS (
                        SELECT 1 FROM pg_constraint 
                        WHERE conname LIKE 'reservas_escritoriodedicado_piso_%'
                        AND conname LIKE '%posicion%'
                    ) THEN
                        EXECUTE (
                            SELECT 'ALTER TABLE reservas_escritoriodedicado DROP CONSTRAINT ' || conname || ';'
                            FROM pg_constraint
                            WHERE conname LIKE 'reservas_escritoriodedicado_piso_%'
                            AND conname LIKE '%posicion%'
                            LIMIT 1
                        );
                    END IF;
                END $$;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
