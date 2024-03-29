# Generated by Django 4.1.1 on 2023-09-06 21:27

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("network_manager", "0006_host_first_discovered_host_last_seen"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="host",
            name="operating_system",
        ),
        migrations.AddField(
            model_name="host",
            name="cpe",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="host",
            name="os_name",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="host",
            name="osclass_type",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.CreateModel(
            name="Port",
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
                ("protocol", models.CharField(max_length=20)),
                ("port_id", models.IntegerField()),
                ("state", models.CharField(max_length=10)),
                ("reason", models.CharField(max_length=20)),
                ("reason_ttl", models.IntegerField()),
                ("service_name", models.CharField(max_length=50)),
                (
                    "service_product",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "service_version",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "service_extra_info",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("service_method", models.CharField(max_length=50)),
                ("service_conf", models.IntegerField()),
                (
                    "service_cpe",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "host",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="network_manager.host",
                    ),
                ),
            ],
            options={
                "unique_together": {("host", "port_id")},
            },
        ),
    ]
