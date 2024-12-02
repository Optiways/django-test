import factory
from datetime import date, datetime, timezone
from faker import Faker

from . import models


fake = Faker(['fr'])


def random_time_zone_for_today():
    today = date.today()
    start_of_day = datetime(today.year, today.month, today.day)
    end_of_day = datetime(today.year, today.month, today.day, 23, 59)
    
    return fake.date_time_between(
        start_date=start_of_day, end_date=end_of_day).replace(
            tzinfo=timezone.utc).astimezone(tz=None)

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
    line = factory.SubFactory('padam_django.apps.geography.factories.BusLineWith5StopFactory')
    
    departure_time = factory.LazyFunction(random_time_zone_for_today)
    arrival_time = factory.LazyFunction(random_time_zone_for_today)

    class Meta:
        model = models.BusShift
