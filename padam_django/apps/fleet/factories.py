import factory
from faker import Faker

from . import models


fake = Faker(["fr"])


class DriverFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory("padam_django.apps.users.factories.UserFactory")

    class Meta:
        model = models.Driver


class BusFactory(factory.django.DjangoModelFactory):
    licence_plate = factory.LazyFunction(fake.license_plate)

    class Meta:
        model = models.Bus


class BusStopFactory(factory.django.DjangoModelFactory):
    name = factory.LazyFunction(fake.address)
    place = factory.SubFactory("padam_django.apps.geography.factories.PlaceFactory")

    class Meta:
        model = models.BusStop
