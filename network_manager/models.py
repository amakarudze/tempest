import uuid as uuid_lib

from django.db import models
from django.urls import reverse


class Host(models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    mac_address = models.CharField(max_length=50, unique=True)
    ipv4_address = models.CharField(max_length=20)
    vendor = models.CharField(max_length=200, blank=True, null=True)
    os_name = models.CharField(max_length=200, blank=True, null=True)
    osclass_type = models.CharField(max_length=200, blank=True, null=True)
    cpe = models.CharField(max_length=200, blank=True, null=True)
    hostname = models.CharField(max_length=50, blank=True, null=True)
    known = models.BooleanField(default=False)
    prohibited = models.BooleanField(default=False)
    status_state = models.CharField(max_length=10)
    status_reason = models.CharField(max_length=20)
    status_reason_ttl = models.CharField(max_length=20)
    first_discovered = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.vendor} - {self.mac_address}"

    def get_absolute_url(self):
        return reverse("host_detail", kwargs={"uuid": self.uuid})


class NmapRun(models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    scanner = models.CharField(max_length=50)
    args = models.CharField(max_length=255)
    start = models.IntegerField()
    startstr = models.CharField(max_length=50)
    version = models.CharField(max_length=10)
    xmloutputversion = models.CharField(max_length=10)
    verbose_level = models.IntegerField()
    debugging_level = models.IntegerField()
    date_run = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.args} - {self.startstr}"

    def get_absolute_url(self):
        return reverse("nmap_run_details", kwargs={"uuid": self.uuid})


class RunStat(models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    nmap_run = models.ForeignKey(NmapRun, on_delete=models.CASCADE)
    finished_time = models.IntegerField()
    finished_timestr = models.DateTimeField()
    finished_summary = models.CharField(max_length=255)
    finished_elapsed = models.FloatField()
    finished_exit = models.CharField(max_length=50)
    finished_errormsg = models.TextField(blank=True, null=True)
    hosts_up = models.IntegerField()
    hosts_down = models.IntegerField()
    hosts_total = models.IntegerField()

    def __str__(self):
        return f"{self.nmap_run} - {self.finished_time}"

    def get_absolute_url(self):
        return reverse("run_stats", kwargs={"uuid": self.uuid})


class Port(models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    protocol = models.CharField(max_length=20)
    port_id = models.IntegerField()
    state = models.CharField(max_length=10)
    reason = models.CharField(max_length=20)
    reason_ttl = models.IntegerField()
    service_name = models.CharField(max_length=50)
    service_product = models.CharField(max_length=50, blank=True, null=True)
    service_version = models.CharField(max_length=50, blank=True, null=True)
    service_extra_info = models.CharField(max_length=255, blank=True, null=True)
    service_method = models.CharField(max_length=50)
    service_conf = models.IntegerField()
    service_cpe = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        unique_together = ["host", "port_id"]

    def __str__(self):
        return f"{self.host} - {self.port_id}"
