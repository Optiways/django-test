from django.test import TestCase
from ..geography.models import Place
from .models import *
from ..geography.factories import PlaceFactory
from ..fleet.factories import DriverFactory, BusFactory


class BusShiftTestCase(TestCase):

    def test_start_before_end(self):
        """
        Testing the BusShift clean() method
        - starting bus stop time before ending bus stop time
        """
        place = PlaceFactory()

        starting_stop = BusStop.objects.create(place=place, time='09:00')
        ending_stop = BusStop.objects.create(place=place, time='10:00')
        bus = BusFactory()
        driver = DriverFactory()

        # Creating shift
        bus_shift = BusShift.objects.create(bus=bus, driver=driver, start=starting_stop, end=ending_stop)

        # Updating shift with wrong inputs
        bus_shift.start = ending_stop
        bus_shift.end = starting_stop

        # Testing if a validation error is raised
        self.assertRaises(ValidationError, bus_shift.clean)

    def test_step_between_start_and_end(self):
        """
        Testing the BusShift clean() method
        - steps are between starting and ending times
        """

    def test_bus_is_available(self):
        """
        Testing the BusShift clean() method
        - the bus is available
        """
        pass

    def test_driver_is_available(self):
        """
        Testing the BusShift clean() method
        - the driver is available
        """



