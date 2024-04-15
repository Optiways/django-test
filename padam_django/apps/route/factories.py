import random
from datetime import timedelta

import factory
from django.utils import timezone

from ..fleet.factories import BusFactory, DriverFactory
from ..geography.factories import PlaceFactory
from .models import BusShift, BusStop


class BusStopFactory(factory.django.DjangoModelFactory):
    """
    A factory for creating BusStop instances.

    Attributes:
        place (factory): A subfactory that creates Place instances.
        transit_time (factory): A Faker that generates a random date_time value.
    """
    place = factory.SubFactory(PlaceFactory)
    transit_time = factory.LazyFunction(
        lambda: timezone.now() + timedelta(days=random.randint(-30, 30), hours=random.randint(0, 23))
    )

    class Meta:
        model = BusStop


class BusShiftFactory(factory.django.DjangoModelFactory):
    """
    A factory for creating BusShift instances.

    Attributes:
        bus (factory): A subfactory that creates Bus instances.
        driver (factory): A subfactory that creates Driver instances.
    """
    class Meta:
        model = BusShift

    bus = factory.SubFactory(BusFactory)
    driver = factory.SubFactory(DriverFactory)
