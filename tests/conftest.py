import pytest

from django.contrib.auth import get_user_model
from django.test import Client

from .factories import DeviceFactory

from network_manager.models import Device


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def user(db):
    user = get_user_model().objects.create_user(
        username="testuser", email="testuser@test.com", password="testpass1234"
    )
    return user


@pytest.fixture
def user_client(user):
    client = Client()
    client.force_login(user)
    return client


@pytest.fixture
def device(db):
    device = DeviceFactory()
    return device


@pytest.fixture
def device1(db):
    device = Device.objects.create(
        name="email-29.baker-salazar.com",
        mac_address="66:d3:cb:e3:81:a2",
        ip_address="172.27.184.68",
    )
    return device


@pytest.fixture
def device_data():
    data = {
        "name": "email-29.baker-salazar.com",
        "mac_address": "66:d3:cb:e3:81:a2",
        "ip_address": "172.27.184.68",
        "device_known": True,
        "device_connected": True,
        "device_prohibited": False,
    }
    return data
