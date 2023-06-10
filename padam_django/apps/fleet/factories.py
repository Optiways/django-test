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


class BusStopFactory(factory.django.DjangoModelFactory):
    place = factory.SubFactory("padam_django.apps.geography.factories.PlaceFactory")
    stop_time = factory.Faker("date_time", tzinfo=timezone.get_current_timezone())

    class Meta:
        model = models.BusStop
