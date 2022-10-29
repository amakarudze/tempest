import factory

from faker import Faker
from faker.providers import internet
from pytest_factoryboy import register

from network_manager.models import Device

fake = Faker()
fake.add_provider(internet)


class DeviceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Device

    uuid = fake.uuid4()
    name = fake.hostname()
    mac_address = fake.mac_address()
    ip_address = fake.ipv4_private()


register(DeviceFactory)
