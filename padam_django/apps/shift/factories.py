from . import models
from padam_django.apps.geography.factories import PlaceFactory
from padam_django.apps.fleet.factories import DriverFactory, BusFactory

import factory
from faker import Faker

fake = Faker(["fr"])


class BusStopFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.BusStop

    name = factory.LazyFunction(fake.name)
    is_transfer_stop = False
    location = factory.SubFactory(PlaceFactory)


class BusStopTimeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.BusStopTime

    transit_time = factory.LazyFunction(fake.time)
    stop = factory.SubFactory(BusStopFactory)


class BusShiftFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.BusShift

    arrival_time = factory.SubFactory(BusStopTimeFactory)
    departure_time = factory.SubFactory(BusStopTimeFactory)
    driver = factory.SubFactory(DriverFactory)
    bus = factory.SubFactory(BusFactory)

    @factory.post_generation
    def bus_stops(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.bus_stops.add(*extracted)
