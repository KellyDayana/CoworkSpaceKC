# Generated migration to remove problematic unique_together

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0004_alter_escritoriodedicado_options_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='escritoriodedicado',
            unique_together=set(),
        ),
    ]
