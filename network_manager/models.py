import uuid as uuid_lib

from django.db import models
from django.urls import reverse


class Device(models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    name = models.CharField(max_length=50)
    mac_address = models.CharField(max_length=50, unique=True)
    ip_address = models.CharField(max_length=20)
    known = models.BooleanField(default=True)
    prohibited = models.BooleanField(default=False)
    device_type = models.CharField(max_length=50, null=True, blank=True)
    up = models.BooleanField(default=False)
    not_shown = models.IntegerField(null=True, blank=True)
    running = models.CharField(max_length=100, null=True, blank=True)
    os_cpe = models.CharField(max_length=100, null=True, blank=True)
    os_details = models.CharField(max_length=100, blank=True, null=True)
    network_distance = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} - {self.mac_address}"

    def get_absolute_url(self):
        return reverse("device_detail", kwargs={"uuid": self.uuid})


class DevicePort(models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    port = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    service = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.device} - {self.port}"
    
    def get_absolute_url(self):
        return reverse("device_port_detail", kwargs={"uuid": self.uuid})
