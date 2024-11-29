import factory
from faker import Faker

from . import models


fake = Faker(['fr'])


class DriverFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory('padam_django.apps.users.factories.UserFactory')

    class Meta:
        model = models.Driver


class BusFactory(factory.django.DjangoModelFactory):
    licence_plate = factory.LazyFunction(fake.license_plate)

    class Meta:
        model = models.Bus


class BusShiftFactory(factory.django.DjangoModelFactory):
    bus = factory.SubFactory(BusFactory)
    driver = factory.SubFactory(DriverFactory)
    start = factory.LazyFunction(fake.date_time_this_month)
    end = factory.LazyFunction(fake.date_time_this_month)
    bus_stop_ids = factory.LazyFunction(lambda: [fake.random_int(min=1, max=100) for _ in range(2)])

    class Meta:
        model = models.BusShift