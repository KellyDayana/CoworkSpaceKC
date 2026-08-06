# Generated manually to fix unique_together constraint issue
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0006_alter_escritoriodedicado_options_and_more'),
    ]

    operations = [
        # Eliminar manualmente el constraint unique_together que causa problemas
        # Usamos múltiples intentos para cubrir diferentes nombres posibles
        migrations.RunSQL(
            sql="""
                -- Intentar eliminar el constraint con el nombre estándar
                ALTER TABLE reservas_escritoriodedicado 
                DROP CONSTRAINT IF EXISTS reservas_escritoriodedicado_piso_posicion_key;
                
                -- Intentar también con el nombre que Django podría generar
                ALTER TABLE reservas_escritoriodedicado 
                DROP CONSTRAINT IF EXISTS reservas_escritoriodedicado_piso_posicion_cd9b3a4f_uniq;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
