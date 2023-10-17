from django.urls import path

from .views import HostDetailView, HomePageView
urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("host/<uuid:uuid>/", HostDetailView.as_view(), name="host_detail"),
]
