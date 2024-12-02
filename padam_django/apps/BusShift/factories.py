import factory
from faker import Faker

from . import models

from padam_django.apps.fleet.factories import BusFactory, DriverFactory

fake = Faker(['fr'])


class BusShiftFactory(factory.django.DjangoModelFactory):

    BusShiftname = factory.LazyFunction(fake.name)
    driver = factory.SubFactory(DriverFactory)
    bus = factory.SubFactory(BusFactory)

    shift_start = factory.LazyFunction(fake.date_time_this_year)
    shift_end = factory.LazyAttribute(
        lambda o: o.shift_start + fake.time_delta())

    @factory.post_generation
    def places(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for place in extracted:
                self.places.add(place)

    class Meta:
        model = models.BusShift
