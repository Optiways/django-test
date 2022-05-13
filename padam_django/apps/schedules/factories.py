import factory
from faker import Faker

from . import models


fake = Faker(['fr'])


class BusShiftFactory(factory.django.DjangoModelFactory):
    driver = factory.SubFactory('padam_django.apps.fleet.factories.DriverFactory')
    bus = factory.SubFactory('padam_django.apps.fleet.factories.BusFactory')
    class Meta:
        model = models.BusShift


class BusStopFactory(factory.django.DjangoModelFactory):
    shift = factory.SubFactory('padam_django.apps.geography.factories.PlaceFactory')
    place = factory.SubFactory('padam_django.apps.schedules.factories.DriverFactory')
    stoptime = fake.time
    class Meta:
        model = models.BusStop