from django.urls import reverse

from pytest_django.asserts import (
    assertRedirects,
    assertTemplateUsed,
)

from network_manager.models import Device


def test_device_model_string_representation():
    device = Device.objects.create(
        name="email-29.baker-salazar.com",
        mac_address="66:d3:cb:e3:81:a2",
        ip_address="172.27.184.68",
    )
    assert str(device) == "email-29.baker-salazar.com - 66:d3:cb:e3:81:a2"


def test_home_view_anonymous_user(client):
    response = client.get(reverse("home"))
    assert response.status_code == 302
    assertRedirects(response, "/accounts/login/?next=/")


def test_home_view_authenticated_user(user_client):
    response = user_client.get(reverse("home"))
    assert response.status_code == 200
    assertTemplateUsed(response, "home.html")


def test_device_details_view_anonymous_user(client, device):
    response = client.get(reverse("device_detail", args=(device.uuid,)))
    assert response.status_code == 302
    assertRedirects(response, f"/accounts/login/?next=/device/{device.uuid}/")


def test_device_details_view_authenticated_user(user_client, device):
    response = user_client.get(reverse("device_detail", args=(device.uuid,)))
    assert response.status_code == 200
    assertTemplateUsed(response, "device_detail.html")


def test_network_traffic_view_anonymous_user(client):
    response = client.get(reverse("network_traffic"))
    assert response.status_code == 302
    assertRedirects(response, "/accounts/login/?next=/network_traffic/")


def test_network_traffic_view_authenticated_user(user_client):
    response = user_client.get(reverse("network_traffic"))
    assert response.status_code == 200
    assertTemplateUsed(response, "network_traffic.html")
