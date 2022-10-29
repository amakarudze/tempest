from django.urls import path

from .views import DeviceDetailView, HomePageView, NetworkTrafficView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("device/<uuid:uuid>/", DeviceDetailView.as_view(), name="device_detail"),
    path("network_traffic/", NetworkTrafficView.as_view(), name="network_traffic"),
]
