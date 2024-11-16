import factory
from faker import Faker

from . import models


fake = Faker(['fr'])
fake_date = fake.date()

# TODO : test
class BusStopFactory(factory.django.DjangoModelFactory):
    place = factory.SubFactory(
        'padam_django.apps.geography.factories.PlaceFactory'
    )
    date_time = fake.datetime_between(fake_date, fake_date)

    class Meta:
        model = models.BusStop


class BusShiftFactory(factory.django.DjangoModelFactory):
    #TODO

    class Meta:
        model = models.BusShift
