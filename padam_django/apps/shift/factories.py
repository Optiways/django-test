from random import randint

import factory
from django.utils import timezone

from padam_django.apps.fleet.factories import BusFactory, DriverFactory
from padam_django.apps.geography.factories import PlaceFactory

from . import models


class BusStopFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: "Bus stop %01d" % n)
    place = factory.SubFactory(PlaceFactory)

    class Meta:
        model = models.BusStop


class BusShiftFactory(factory.django.DjangoModelFactory):
    bus = factory.SubFactory(BusFactory)
    driver = factory.SubFactory(DriverFactory)
    first_stop = timezone.now()
    last_stop = timezone.now()

    class Meta:
        model = models.BusShift


class ScheduleStopFactory(factory.django.DjangoModelFactory):
    bus_shift = factory.SubFactory(BusShiftFactory)
    bus_stop = factory.SubFactory(BusStopFactory)
    arrival = timezone.now() + timezone.timedelta(hours=randint(7, 22))

    class Meta:
        model = models.ScheduleStop
