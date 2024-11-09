from django.db import IntegrityError, transaction
from django.db.models import QuerySet
from django.test import TestCase
from .models import BusStop, BusShift, BusShiftStops
from ..fleet.factories import DriverFactory, BusFactory
from ..fleet.models import Driver, Bus
from ..geography.factories import PlaceFactory
from ..geography.models import Place
from ..users.factories import UserFactory


# Create your tests here.
class BusStopsTestCase(TestCase):
    def test_create(self):
        PlaceFactory.create_batch(size=10)
        places: QuerySet = Place.objects.all()[2:7]
        stops: list[BusStop] = []

        for place in places:
            stop = BusStop(place.name, place)
            stops.append(stop)


class BusShiftTestCase(TestCase):
    def test_create(self):
        UserFactory.create_batch(size=10)
        DriverFactory.create_batch(size=5)
        BusFactory.create_batch(size=5)

        driver: Driver = Driver.objects.filter()[1]
        bus: Bus = Bus.objects.filter()[1]

        stops = BusStop.objects.filter()[0:4]

        start_time_0 = '01:00:00'
        end_time_0 = '02:00:00'

        start_time_1 = '11:00:00'
        end_time_1 = '12:00:00'

        start_time_2 = '21:00:00'
        end_time_2 = '22:00:00'

        bs0: BusShift = BusShift(driver=driver, bus=bus, start_time=start_time_0, end_time=end_time_0)
        bs0.save()

        bs2: BusShift = BusShift(driver=driver, bus=bus, start_time=start_time_2, end_time=end_time_2)
        bs2.save()

        bs1: BusShift = BusShift(driver=driver, bus=bus, start_time=start_time_1, end_time=end_time_1)
        bs1.save()

        e0: BusShift = BusShift(driver=driver, bus=bus, start_time=end_time_0, end_time=start_time_0)
        try:
            with transaction.atomic():
                e0.save()
            self.fail("end before start")
        except IntegrityError:
            pass

        # TODO test form
        # Those tests will fail because they don't use the form that checks for overlapping schedules
        e1: BusShift = BusShift(driver=driver, bus=bus, start_time=start_time_0, end_time=end_time_2)
        try:
            with transaction.atomic():
                e1.save()
            self.fail("No concurrent shifts allowed")
        except IntegrityError:
            pass

        e2: BusShift = BusShift(driver=driver, bus=bus, start_time=start_time_0, end_time=end_time_2)
        try:
            with transaction.atomic():
                e2.save()
            self.fail("No concurrent shifts allowed")
        except IntegrityError:
            pass