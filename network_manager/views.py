from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic.edit import UpdateView

from .models import Host, NmapRun, Port, RunStat


class HomePageView(LoginRequiredMixin, ListView):
    template_name = "home.html"
    model = Host

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        nmap_run = NmapRun.objects.all().order_by("-date_run").first()
        context["nmap_run"] = nmap_run
        try:
            runstats = RunStat.objects.get(nmap_run=nmap_run)
        except RunStat.DoesNotExist:
            runstats = ""
        context["runstats"] = runstats
        return context


class HostDetailView(LoginRequiredMixin, UpdateView):
    slug_url_kwarg = "uuid"
    slug_field = "uuid"
    template_name = "device_detail.html"
    model = Host
    fields = (
        "vendor",
        "hostname",
        "ipv4_address",
        "known",
        "prohibited",
    )
    context_object_name = "host"
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        uuid = self.kwargs.get("uuid")
        context["uuid"] = uuid
        context["ports"] = Port.objects.prefetch_related('host').filter(host=uuid)
        return context
