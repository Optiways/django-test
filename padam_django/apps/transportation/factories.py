import factory
from faker import Faker
from transportation import models as transportation_models
from geography.factories import PlaceFactory
from fleet.factories import BusFactory, DriverFactory
from datetime import datetime, timedelta

fake = Faker(['fr'])

def generate_random_time_today():
    today = datetime.today().date()
    random_time = fake.time_object()
    return datetime.combine(today, random_time)

class BusStopFactory(factory.django.DjangoModelFactory):
    place = factory.SubFactory(PlaceFactory)
    arrival_time = factory.LazyFunction(generate_random_time_today)

    class Meta:
        model = transportation_models.BusStop

class BusShiftFactory(factory.django.DjangoModelFactory):
    bus = factory.SubFactory(BusFactory)
    driver = factory.SubFactory(DriverFactory)

    @factory.post_generation
    def stops(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for stop in extracted:
                self.stops.add(stop)
        else:
            self.stops.add(BusStopFactory(), BusStopFactory())

    class Meta:
        model = transportation_models.BusShift