# Migración para cambiar de posicion_x/posicion_y a posicion única
from django.db import migrations, models, connection


def verificar_y_migrar_posiciones(apps, schema_editor):
    """Copiar posicion_x a posicion si posicion_x existe"""
    # Verificar si posicion_x existe
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='reservas_escritoriodedicado' 
            AND column_name='posicion_x'
        """)
        posicion_x_existe = cursor.fetchone() is not None
    
    if posicion_x_existe:
        EscritorioDedicado = apps.get_model('reservas', 'EscritorioDedicado')
        for escritorio in EscritorioDedicado.objects.all():
            escritorio.posicion = escritorio.posicion_x
            escritorio.save()


def verificar_columna_existe(tabla, columna):
    """Verifica si una columna existe en una tabla"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name=%s AND column_name=%s
        """, [tabla, columna])
        return cursor.fetchone() is not None


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0003_alter_escritoriodedicado_posicion_fields_unique'),
    ]

    operations = [
        # 1. Agregar el nuevo campo posicion solo si no existe
        migrations.RunSQL(
            sql="""
                DO $$ 
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns 
                        WHERE table_name='reservas_escritoriodedicado' AND column_name='posicion'
                    ) THEN
                        ALTER TABLE reservas_escritoriodedicado ADD COLUMN posicion integer DEFAULT 1 NOT NULL;
                    END IF;
                END $$;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
        # 2. Copiar datos de posicion_x a posicion si existe posicion_x
        migrations.RunPython(verificar_y_migrar_posiciones, reverse_code=migrations.RunPython.noop),
        # 3. Eliminar el constraint antiguo si existe
        migrations.RunSQL(
            sql="""
                DO $$ 
                BEGIN
                    IF EXISTS (
                        SELECT 1 FROM pg_constraint 
                        WHERE conname='reservas_escritoriod_piso_posicion_x_posic_7a9fe5a4_uniq'
                    ) THEN
                        ALTER TABLE reservas_escritoriodedicado 
                        DROP CONSTRAINT reservas_escritoriod_piso_posicion_x_posic_7a9fe5a4_uniq;
                    END IF;
                END $$;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
        # 4. Eliminar campos antiguos si existen
        migrations.RunSQL(
            sql="""
                DO $$ 
                BEGIN
                    IF EXISTS (
                        SELECT 1 FROM information_schema.columns 
                        WHERE table_name='reservas_escritoriodedicado' AND column_name='posicion_x'
                    ) THEN
                        ALTER TABLE reservas_escritoriodedicado DROP COLUMN posicion_x;
                    END IF;
                    IF EXISTS (
                        SELECT 1 FROM information_schema.columns 
                        WHERE table_name='reservas_escritoriodedicado' AND column_name='posicion_y'
                    ) THEN
                        ALTER TABLE reservas_escritoriodedicado DROP COLUMN posicion_y;
                    END IF;
                END $$;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
        # 5. Agregar el nuevo constraint si no existe
        migrations.RunSQL(
            sql="""
                DO $$ 
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM pg_constraint 
                        WHERE conname='reservas_escritoriod_piso_posicion_uniq'
                    ) THEN
                        ALTER TABLE reservas_escritoriodedicado 
                        ADD CONSTRAINT reservas_escritoriod_piso_posicion_uniq 
                        UNIQUE (piso, posicion);
                    END IF;
                END $$;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
