import factory
from padam_django.apps.geography.factories import PlaceFactory
from datetime import datetime, timedelta
from random import randint

from padam_django.apps.pathing.models import BusStop
from django.utils.timezone import make_aware

def futur_datetime():
    return make_aware(datetime.now() + timedelta(days=randint(1, 30)))

class BusStopFactory(factory.django.DjangoModelFactory):
    visit_date_time = factory.LazyFunction(futur_datetime)
    place = factory.SubFactory(PlaceFactory)

    class Meta:
        model = BusStop