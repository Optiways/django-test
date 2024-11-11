from datetime import time

import factory
from faker import Faker

from . import models

fake = Faker(['fr'])


class PlaceFactory(factory.django.DjangoModelFactory):
    name = factory.LazyFunction(fake.street_name)

    longitude = factory.LazyFunction(fake.longitude)
    latitude = factory.LazyFunction(fake.latitude)

    class Meta:
        model = models.Place


class BusStopFactory(factory.django.DjangoModelFactory):
    place = factory.SubFactory(PlaceFactory)
    expected_arrival = factory.LazyFunction(
        lambda: time(hour=fake.random_int(min=0, max=23), minute=fake.random_int(min=0, max=59)))

    class Meta:
        model = models.BusStop
