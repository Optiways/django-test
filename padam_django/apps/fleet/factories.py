import factory
from faker import Faker

from padam_django.apps.fleet import models
from padam_django.apps.geography.factories import PlaceFactory

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
    bus = factory.SubFactory(BusFactory)
    place = factory.SubFactory(PlaceFactory)
    departure_time = factory.LazyFunction(fake.time)

    class Meta:
        model = models.BusStop


class BusShiftFactory(factory.django.DjangoModelFactory):
    bus = factory.SubFactory(BusFactory)
    driver = factory.SubFactory(DriverFactory)
    departure_time = factory.LazyFunction(fake.time)
    arrival_time = factory.LazyFunction(fake.time)

    class Meta:
        model = models.BusShift
