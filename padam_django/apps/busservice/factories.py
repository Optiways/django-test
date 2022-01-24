from datetime import datetime
import factory
from padam_django.apps.busservice.models import BusShift, BusStop
from padam_django.apps.geography.factories import PlaceFactory
from padam_django.apps.fleet.factories import BusFactory, DriverFactory


class BusShiftFactory(factory.django.DjangoModelFactory):

    driver = factory.SubFactory(DriverFactory)
    bus = factory.SubFactory(BusFactory)

    class Meta:
        model = BusShift


class BusStopFactory(factory.django.DjangoModelFactory):

    place = factory.SubFactory(PlaceFactory)
    timestamp = datetime.now()
    busshift = factory.SubFactory(BusShiftFactory)

    class Meta:
        model = BusStop
