# Migration to change from (posicion_x, posicion_y) to single horizontal position (1-10)

from django.db import migrations, models


def migrar_posiciones_existentes(apps, schema_editor):
    EscritorioDedicado = apps.get_model('reservas', 'EscritorioDedicado')
    
    escritorios_por_piso = {}
    for escritorio in EscritorioDedicado.objects.all().order_by('piso', 'id'):
        piso = escritorio.piso
        if piso not in escritorios_por_piso:
            escritorios_por_piso[piso] = []
        escritorios_por_piso[piso].append(escritorio)
    
    for piso, escritorios in escritorios_por_piso.items():
        for idx, escritorio in enumerate(escritorios, start=1):
            if idx <= 10:
                escritorio.posicion = idx
                escritorio.save(update_fields=['posicion'])


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0003_alter_escritoriodedicado_posicion_fields_unique'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='escritoriodedicado',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='escritoriodedicado',
            name='posicion',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.RunPython(migrar_posiciones_existentes, reverse_code=migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='escritoriodedicado',
            name='posicion_x',
        ),
        migrations.RemoveField(
            model_name='escritoriodedicado',
            name='posicion_y',
        ),
        migrations.AlterUniqueTogether(
            name='escritoriodedicado',
            unique_together={('piso', 'posicion')},
        ),
        migrations.AlterModelOptions(
            name='escritoriodedicado',
            options={'ordering': ['piso', 'posicion']},
        ),
    ]
