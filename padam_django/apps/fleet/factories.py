from datetime import datetime
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
    time = datetime.now()
    place = factory.SubFactory("padam_django.apps.geography.factories.PlaceFactory")
    shift = factory.SubFactory("padam_django.apps.fleet.factories.BusShiftFactory")

    class Meta:
        model = models.BusStop


class BusShiftFactory(factory.django.DjangoModelFactory):
    bus = factory.SubFactory("padam_django.apps.fleet.factories.BusFactory")
    driver = factory.SubFactory("padam_django.apps.fleet.factories.DriverFactory")

    class Meta:
        model = models.BusShift
