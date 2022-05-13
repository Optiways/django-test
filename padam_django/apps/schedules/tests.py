import datetime
import django_perf_rec
from django.test import TestCase
from padam_django.apps.schedules.factories import BusShiftFactory, BusStopFactory
from padam_django.apps.schedules.models import BusShift


class BusShiftTestCase(TestCase):
    def _dummy_shift(self, start, end, bus=None, driver=None):
        kwargs = {}
        if bus is not None:
            kwargs["bus"] = bus
        if driver is not None:
            kwargs["driver"] = driver
        shift = BusShiftFactory(**kwargs)
        BusStopFactory(shift=shift, stoptime=datetime.time(start))
        BusStopFactory(shift=shift, stoptime=datetime.time(end))
        return shift

    def test_available_shift(self):
        """
        Shift is available
        """
        # create a shift between 8h00 and 10h00
        shift = self._dummy_shift(start=8, end=10)

        # create a shift between 15h00 and 18h00
        self._dummy_shift(start=15, end=18, bus=shift.bus, driver=shift.driver)

        # for a new shift, check if there's already an available shift
        # between 11h00 and 12h00
        next_shift = BusShiftFactory(bus=shift.bus, driver=shift.driver)
        with django_perf_rec.record():
            assert next_shift.shift_is_available(
                start_time=datetime.time(11), end_time=datetime.time(12)
            )

    def test_available_shift_collides_different_bus_driver(self):
        """
        Shift collides but with different bus and driver, should be available
        """
        # create a shift between 8h00 and 11h00
        shift = self._dummy_shift(start=8, end=11)

        next_shift = BusShiftFactory()

        assert shift.bus != next_shift.bus
        assert shift.driver != next_shift.driver

        # check shift between 9h00 and 10h00
        assert next_shift.shift_is_available(
            start_time=datetime.time(9), end_time=datetime.time(10)
        )

    def test_available_shift_collides(self):
        """
        Shift collides for the bus:
        - start time collides
        - end time collides
        - both start and end collides
        """
        next_shift = BusShiftFactory()
        cases = [(8, 10), (10, 13), (8, 13)]

        # existing shift from 9h00 to 12h00
        shift = self._dummy_shift(start=9, end=12, bus=next_shift.bus)

        for start, end in cases:
            assert not next_shift.shift_is_available(
                start_time=datetime.time(start), end_time=datetime.time(end)
            )
