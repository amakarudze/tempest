import nmap

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from django.views.generic.base import TemplateView

from .models import Device


class HomePageView(LoginRequiredMixin, ListView):
    template_name = "home.html"
    model = Device


class DeviceDetailView(LoginRequiredMixin, UpdateView):
    slug_url_kwarg = "uuid"
    slug_field = "uuid"
    template_name = "device_detail.html"
    model = Device
    fields = (
        "name",
        "mac_address",
        "ip_address",
        "device_known",
        "device_connected",
        "device_prohibited",
    )
    context_object_name = "device"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["uuid"] = self.kwargs.get("uuid")
        return context


class NetworkTrafficView(LoginRequiredMixin, TemplateView):
    template_name = "network_traffic.html"
    model = Device

    def get_context_data(self, **kwargs):
        nm = nmap.PortScanner()
        network_hosts = nm.scan('192.168.1.0/24', arguments='-O --osscan-guess --privileged')
        context = super().get_context_data(**kwargs)
        context["network_hosts"] = network_hosts
        return context


class DeviceDetailView(LoginRequiredMixin, UpdateView):
    slug_url_kwarg = "uuid"
