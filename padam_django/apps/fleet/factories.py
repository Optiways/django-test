import factory
from faker import Faker

from . import models
from datetime import datetime, timezone

fake = Faker(['fr'])


class DriverFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory('padam_django.apps.users.factories.UserFactory')

    class Meta:
        model = models.Driver


class BusFactory(factory.django.DjangoModelFactory):
    licence_plate = factory.LazyFunction(fake.license_plate)

    class Meta:
        model = models.Bus

class BusShiftFactory(factory.django.DjangoModelFactory):
    name = factory.LazyFunction(fake.name)
    bus = factory.SubFactory(BusFactory)
    driver = factory.SubFactory(DriverFactory)

    class Meta:
        model = models.BusShift

class BusStopFactory(factory.django.DjangoModelFactory):
    name = factory.LazyFunction(fake.name)
    time = fake.date_time_between_dates(
        datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        datetime(2024, 1, 1, 23, 59, 59, tzinfo=timezone.utc)
    )
    place = factory.SubFactory('padam_django.apps.geography.factories.PlaceFactory')
    bus_shift = factory.SubFactory(BusShiftFactory)

    class Meta:
        model = models.BusStop
