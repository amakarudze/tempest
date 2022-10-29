import pytest

from django.contrib.auth import get_user_model
from django.test import Client

from .factories import DeviceFactory


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
