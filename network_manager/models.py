import uuid as uuid_lib

from django.db import models
from django.urls import reverse


class Device(models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    name = models.CharField(max_length=50)
    mac_address = models.CharField(max_length=50, unique=True)
    ip_address = models.CharField(max_length=20)
    device_known = models.BooleanField(default=True)
    device_prohibited = models.BooleanField(default=False)
    device_connected = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.mac_address}"

    def get_absolute_url(self):
        return reverse("device_detail", kwargs={"uuid": self.uuid})
