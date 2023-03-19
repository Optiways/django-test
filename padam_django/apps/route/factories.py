import factory
from django.utils import timezone

from . import models
from ..fleet.factories import BusFactory, DriverFactory
from ..geography.factories import PlaceFactory


class BusShiftFactory(factory.django.DjangoModelFactory):
    bus = factory.SubFactory(BusFactory)
    driver = factory.SubFactory(DriverFactory)
    departure_time = timezone.now()
    arrival_time = timezone.now() + timezone.timedelta(hours=3)

    class Meta:
        model = models.BusShift


class BusStopFactory(factory.django.DjangoModelFactory):
    place = factory.SubFactory(PlaceFactory)
    passage_time = timezone.now()
    bus_shift = factory.SubFactory(BusShiftFactory)

    class Meta:
        model = models.BusStop
