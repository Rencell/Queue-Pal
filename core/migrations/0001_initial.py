# Generated by Django 5.1.4 on 2025-01-30 10:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

def add_status_data(apps, schema_editor):
    
    Group = apps.get_model('auth', 'group')
    group_staff, created = Group.objects.get_or_create(name='Staff')
    
    Status = apps.get_model('core', 'Status')
    RoomStatus = apps.get_model('core', 'RoomStatus')
    Status.objects.create(name="PENDING", description="default pending")
    Status.objects.create(name="COMPLETED", description="current serving")
    Status.objects.create(name="CANCELLED", description="ended session or cancelled")
    Status.objects.create(name="NO_SHOW", description="did not show")
    Status.objects.create(name="WAITING", description="being waited")
    Status.objects.create(name="PHYSICAL QUEUE", description="queue on physical")

    RoomStatus.objects.create(name="ACTIVE")
    RoomStatus.objects.create(name="PAUSED")
    RoomStatus.objects.create(name="TERMINATED")
    
class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='RoomStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notificationEnabled', models.BooleanField(default=True)),
                ('summon_queue_number', models.PositiveIntegerField(default=10)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True)),
                ('current_serving_queue_number', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status_description', models.TextField(default=1)),
                ('status_time', models.CharField(default=1, max_length=50)),
                ('status_evaluated_time', models.CharField(default=1, max_length=50)),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('status', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.roomstatus')),
            ],
            options={
                'unique_together': {('staff', 'code')},
            },
        ),
        migrations.CreateModel(
            name='UserRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('queue_number', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('issue', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.issue')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.room')),
                ('status', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.status')),
                ('user', models.ForeignKey(blank=True, default='Anonymous', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        
        migrations.RunPython(add_status_data),
    ]
