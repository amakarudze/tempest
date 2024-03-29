# Generated by Django 4.1.1 on 2023-07-19 15:39

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("network_manager", "0002_rename_ip_number_device_ip_address_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Host",
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
                ("mac_address", models.CharField(max_length=50, unique=True)),
                ("ipv4_address", models.CharField(max_length=20)),
                ("vendor", models.CharField(max_length=200)),
                ("hostname", models.CharField(blank=True, max_length=50, null=True)),
                ("known", models.BooleanField(default=False)),
                ("prohibited", models.BooleanField(default=False)),
                ("status_state", models.CharField(max_length=10)),
                ("status_reason", models.CharField(max_length=20)),
                ("status_reason_ttl", models.CharField(max_length=20)),
                ("times_srtt", models.IntegerField()),
                ("times_rttvar", models.IntegerField()),
                ("times_to", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="NmapRun",
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
                ("scanner", models.CharField(max_length=50)),
                ("args", models.CharField(max_length=255)),
                ("start", models.IntegerField()),
                ("startstr", models.CharField(max_length=50)),
                ("version", models.CharField(max_length=10)),
                ("xmloutputversion", models.CharField(max_length=10)),
                ("verbose_level", models.IntegerField()),
                ("debugging_level", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="RunStat",
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
                ("finished_time", models.IntegerField()),
                ("finished_timestr", models.DateTimeField()),
                ("finished_summary", models.CharField(max_length=255)),
                ("finished_elapsed", models.FloatField()),
                ("finished_exit", models.CharField(max_length=50)),
                ("hosts_up", models.IntegerField()),
                ("hosts_down", models.IntegerField()),
                ("hosts_total", models.IntegerField()),
                (
                    "nmap_run",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="network_manager.nmaprun",
                    ),
                ),
            ],
        ),
        migrations.RemoveField(
            model_name="deviceport",
            name="device",
        ),
        migrations.DeleteModel(
            name="Device",
        ),
        migrations.DeleteModel(
            name="DevicePort",
        ),
    ]
