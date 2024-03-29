# Generated by Django 4.1.1 on 2023-03-21 17:48

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("network_manager", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="device",
            old_name="ip_number",
            new_name="ip_address",
        ),
        migrations.RenameField(
            model_name="device",
            old_name="device_known",
            new_name="known",
        ),
        migrations.RenameField(
            model_name="device",
            old_name="device_connected",
            new_name="prohibited",
        ),
        migrations.RenameField(
            model_name="device",
            old_name="device_prohibited",
            new_name="up",
        ),
        migrations.AddField(
            model_name="device",
            name="device_type",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="device",
            name="network_distance",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="device",
            name="not_shown",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="device",
            name="os_cpe",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="device",
            name="os_details",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="device",
            name="running",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.CreateModel(
            name="DevicePort",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uuid",
                    models.UUIDField(db_index=True, default=uuid.uuid4, editable=False),
                ),
                ("port", models.CharField(max_length=20)),
                ("state", models.CharField(max_length=20)),
                ("service", models.CharField(max_length=50)),
                (
                    "device",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="network_manager.device",
                    ),
                ),
            ],
        ),
    ]
