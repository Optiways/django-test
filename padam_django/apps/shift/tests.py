from django.test import TestCase
from django.utils import timezone

from padam_django.apps.fleet.factories import BusFactory, DriverFactory
from padam_django.apps.shift.factories import (
    BusShiftFactory,
    BusStopFactory,
    ScheduleStopFactory,
)
from padam_django.apps.shift.forms import ScheduleStopForm


class BusShiftTests(TestCase):
    def setUp(self):
        self.bus = BusFactory()
        self.driver = DriverFactory()

    def test_create_shift_and_schedule_success(self):
        """
        Test if creation of shift and schedule works.
        """
        initial_datetime = timezone.now()
        bus_stop = BusStopFactory()
        bus_shift = BusShiftFactory(bus=self.bus, driver=self.driver)
        ScheduleStopFactory(
            bus_shift=bus_shift, bus_stop=bus_stop, arrival=initial_datetime
        )

        # try to create a new ScheduleStop instance
        form = ScheduleStopForm(
            data={
                "bus_shift": bus_shift,
                "bus_stop": bus_stop,
                "arrival": initial_datetime + timezone.timedelta(hours=2),
            }
        )

        self.assertTrue(form.is_valid())

    def test_create_shift_and_schedule_error_bus_not_available(self):
        """
        Test if bus shifts overlap.
        """
        initial_datetime = timezone.now()
        bus_stop = BusStopFactory()
        bus_shift = BusShiftFactory(bus=self.bus, driver=self.driver)
        ScheduleStopFactory(
            bus_shift=bus_shift, bus_stop=bus_stop, arrival=initial_datetime
        )
        ScheduleStopFactory(
            bus_shift=bus_shift,
            bus_stop=bus_stop,
            arrival=initial_datetime + timezone.timedelta(hours=3),
        )

        # try to create a new ScheduleStop instance
        form = ScheduleStopForm(
            data={
                "bus_shift": bus_shift,
                "bus_stop": bus_stop,
                "arrival": initial_datetime + timezone.timedelta(hours=2),
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("Bus is not available", form.errors["__all__"][0])

    def test_create_shift_and_schedule_error_driver_not_available(self):
        """
        Test if driver shifts overlap.
        """
        initial_datetime = timezone.now()
        new_bus = BusFactory()
        bus_stop = BusStopFactory()
        bus_shift = BusShiftFactory(bus=self.bus, driver=self.driver)
        new_bus_shift = BusShiftFactory(bus=new_bus, driver=self.driver)
        ScheduleStopFactory(
            bus_shift=new_bus_shift, bus_stop=bus_stop, arrival=initial_datetime
        )
        ScheduleStopFactory(
            bus_shift=new_bus_shift,
            bus_stop=bus_stop,
            arrival=initial_datetime + timezone.timedelta(hours=3),
        )

        # try to create a new ScheduleStop instance
        form = ScheduleStopForm(
            data={
                "bus_shift": bus_shift,
                "bus_stop": bus_stop,
                "arrival": initial_datetime + timezone.timedelta(hours=2),
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("Driver is not available", form.errors["__all__"][0])
