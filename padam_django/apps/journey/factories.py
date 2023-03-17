import factory
from faker import Faker

from . import models


fake = Faker(['fr'])


class BusShiftFactory(factory.django.DjangoModelFactory):
    bus = factory.SubFactory('padam_django.apps.fleet.factories.BusFactory')
    driver = factory.SubFactory(
        'padam_django.apps.fleet.factories.DriverFactory')
    bus_stops = factory.SubFactory(
        'padam_django.apps.journey.factories.BusStopFactory')
    start_time = factory.LazyFunction(fake.start_time)
    end_time = factory.LazyFunction(fake.end_time)
    shift_duration = factory.LazyFunction(fake.shift_duration)

    class Meta:
        model = models.BusShift


class BusStopFactory(factory.django.DjangoModelFactory):
    licence_plate = factory.LazyFunction(fake.license_plate)
    place = factory.SubFactory(
        'padam_django.apps.geography.factories.PlaceFactory')
    passing_time = factory.LazyFunction(fake.passing_time)

    class Meta:
        model = models.BusStop
