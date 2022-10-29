from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateView

from .models import Device


class HomePageView(LoginRequiredMixin, ListView):
    template_name = "home.html"
    model = Device


class DeviceDetailView(LoginRequiredMixin, DetailView):
    slug_url_kwarg = "uuid"
    slug_field = "uuid"
    template_name = "device_detail.html"
    model = Device
    context_object_name = "device"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["uuid"] = self.kwargs.get("uuid")
        return context


class NetworkTrafficView(LoginRequiredMixin, TemplateView):
    template_name = "network_traffic.html"
