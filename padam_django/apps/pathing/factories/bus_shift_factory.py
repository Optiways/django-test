import factory
from factory import django, List, SubFactory, LazyAttribute
from padam_django.apps.fleet.factories import BusFactory, DriverFactory
from padam_django.apps.pathing.factories.bus_stop_factory import BusStopFactory
from padam_django.apps.pathing.models import BusShift


class BusShiftFactory(django.DjangoModelFactory):
    bus = factory.SubFactory(BusFactory)
    driver = factory.SubFactory(DriverFactory)
    bus_stops = factory.RelatedFactoryList(
        BusStopFactory,
        factory_related_name='bus_shift',
        size=2
    )

    class Meta:
        model = BusShift