import factory
from faker import Faker
from django.conf import settings
import pytz
from datetime import datetime, timedelta

from . import models


fake = Faker(["fr"])


class BusShiftFactory(factory.django.DjangoModelFactory):
    driver = factory.SubFactory("padam_django.apps.fleet.factories.DriverFactory")
    bus = factory.SubFactory("padam_django.apps.fleet.factories.BusFactory")

    class Meta:
        model = models.BusShift


class BusStopFactory(factory.django.DjangoModelFactory):
    place = factory.SubFactory("padam_django.apps.geography.factories.PlaceFactory")
    # fixme: Faker gen the same datetime in a batch
    stop_datetime = fake.date_time_between(tzinfo=pytz.timezone(settings.TIME_ZONE),
                                           start_date=datetime.now(),
                                           end_date=datetime.now() + timedelta(days=1))

    class Meta:
        model = models.BusStop
