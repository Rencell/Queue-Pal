# Generated by Django 5.1.4 on 2025-01-02 12:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_alter_room_status'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.roomstatus'),
        ),
        migrations.AlterUniqueTogether(
            name='room',
            unique_together={('staff', 'code')},
        ),
    ]
