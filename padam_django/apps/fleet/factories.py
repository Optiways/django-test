import factory
from faker import Faker
from django.utils import timezone

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


class BusShiftFactory(factory.django.DjangoModelFactory):
    bus = factory.SubFactory("padam_django.apps.fleet.factories.BusFactory")
    driver = factory.SubFactory("padam_django.apps.fleet.factories.DriverFactory")
    start_time = factory.Faker("date_time", tzinfo=timezone.get_current_timezone())
    end_time = factory.Faker("date_time", tzinfo=timezone.get_current_timezone())

    class Meta:
        model = models.BusShift


class BusStopFactory(factory.django.DjangoModelFactory):
    place = factory.SubFactory("padam_django.apps.geography.factories.PlaceFactory")
    datetime = factory.Faker("date_time", tzinfo=timezone.get_current_timezone())
    shift = factory.SubFactory("padam_django.apps.fleet.factories.BusShiftFactory")

    class Meta:
        model = models.BusStop
