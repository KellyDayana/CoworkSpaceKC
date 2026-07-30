# Migration to change from (posicion_x, posicion_y) to single horizontal position (1-10)
# This simplifies the system to 10 horizontal positions per floor

from django.db import migrations, models


def migrar_posiciones_existentes(apps, schema_editor):
    """
    Migra los datos existentes:
    - Agrupa escritorios por piso
    - Asigna posiciones 1-10 secuencialmente según orden de creación
    """
    EscritorioDedicado = apps.get_model('reservas', 'EscritorioDedicado')
    
    # Agrupar por piso
    escritorios_por_piso = {}
    for escritorio in EscritorioDedicado.objects.all().order_by('piso', 'id'):
        piso = escritorio.piso
        if piso not in escritorios_por_piso:
            escritorios_por_piso[piso] = []
        escritorios_por_piso[piso].append(escritorio)
    
    # Asignar posiciones secuenciales (1-10) por piso
    for piso, escritorios in escritorios_por_piso.items():
        for idx, escritorio in enumerate(escritorios, start=1):
            if idx <= 10:  # Máximo 10 posiciones
                escritorio.posicion = idx
                escritorio.save(update_fields=['posicion'])


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0003_alter_escritoriodedicado_posicion_fields_unique'),
    ]

    operations = [
        # Remove old unique_together constraint first
        migrations.AlterUniqueTogether(
            name='escritoriodedicado',
            unique_together=set(),
        ),
        # Add new single position field (without unique constraint yet)
        migrations.AddField(
            model_name='escritoriodedicado',
            name='posicion',
            field=models.PositiveIntegerField(default=1),
        ),
        # Migrate existing data
        migrations.RunPython(migrar_posiciones_existentes, reverse_code=migrations.RunPython.noop),
        # Remove old position fields
        migrations.RemoveField(
            model_name='escritoriodedicado',
            name='posicion_x',
        ),
        migrations.RemoveField(
            model_name='escritoriodedicado',
            name='posicion_y',
        ),
        # Now add unique_together constraint for (piso, posicion)
        migrations.AlterUniqueTogether(
            name='escritoriodedicado',
            unique_together={('piso', 'posicion')},
        ),
        # Add ordering
        migrations.AlterModelOptions(
            name='escritoriodedicado',
            options={'ordering': ['piso', 'posicion']},
        ),
    ]
