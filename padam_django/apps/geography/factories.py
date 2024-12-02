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
    name = factory.LazyFunction(fake.street_name)
    place = factory.SubFactory(PlaceFactory)

    class Meta:
        model = models.BusStop

class BusLineFactory(factory.django.DjangoModelFactory):
    number = factory.LazyFunction(lambda: fake.pyint(min_value=0, max_value=300))

    class Meta:
        model = models.BusLine

class BusLineStopFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.BusLineStop

    stop = factory.SubFactory(BusStopFactory)
    line = factory.SubFactory(BusLineFactory)
    sequence = factory.LazyFunction(lambda: fake.pyint(min_value=0, max_value=100))

class BusLineWith5StopFactory(BusLineFactory):
    line_stop1 = factory.RelatedFactory(
        BusLineStopFactory,
        factory_related_name='line')
    line_stop2 = factory.RelatedFactory(
        BusLineStopFactory,
        factory_related_name='line')
    line_stop3 = factory.RelatedFactory(
        BusLineStopFactory,
        factory_related_name='line')
    line_stop4 = factory.RelatedFactory(
        BusLineStopFactory,
        factory_related_name='line')
    line_stop5 = factory.RelatedFactory(
        BusLineStopFactory,
        factory_related_name='line')
