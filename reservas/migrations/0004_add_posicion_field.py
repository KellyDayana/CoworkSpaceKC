# Migración para cambiar de posicion_x/posicion_y a posicion única
from django.db import migrations, models


def migrar_posiciones(apps, schema_editor):
    """Copiar posicion_x a posicion"""
    EscritorioDedicado = apps.get_model('reservas', 'EscritorioDedicado')
    for escritorio in EscritorioDedicado.objects.all():
        escritorio.posicion = escritorio.posicion_x
        escritorio.save()


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0003_alter_escritoriodedicado_posicion_fields_unique'),
    ]

    operations = [
        # 1. Agregar el nuevo campo posicion
        migrations.AddField(
            model_name='escritoriodedicado',
            name='posicion',
            field=models.PositiveIntegerField(default=1),
        ),
        # 2. Copiar datos de posicion_x a posicion
        migrations.RunPython(migrar_posiciones, reverse_code=migrations.RunPython.noop),
        # 3. Eliminar el constraint antiguo
        migrations.AlterUniqueTogether(
            name='escritoriodedicado',
            unique_together=set(),
        ),
        # 4. Eliminar campos antiguos
        migrations.RemoveField(
            model_name='escritoriodedicado',
            name='posicion_x',
        ),
        migrations.RemoveField(
            model_name='escritoriodedicado',
            name='posicion_y',
        ),
        # 5. Agregar el nuevo constraint
        migrations.AlterUniqueTogether(
            name='escritoriodedicado',
            unique_together={('piso', 'posicion')},
        ),
        # 6. Agregar Meta options
        migrations.AlterModelOptions(
            name='escritoriodedicado',
            options={'ordering': ['piso', 'posicion']},
        ),
    ]
