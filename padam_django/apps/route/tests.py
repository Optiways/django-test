from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from .models import BusShift
from ..fleet.factories import BusFactory, DriverFactory
from .factories import BusShiftFactory


class TestBusShift(TestCase):

    def setUp(self) -> None:
        self.bus = BusFactory()
        self.driver = DriverFactory()

    def test_no_overlapping_shifts(self) -> None:
        """test that two BusShift can not have the same driver or bus when the start and end times overlap """

        # CASE 1: A BusShift that starts in the future is already scheduled
        BusShiftFactory.create(
            bus=self.bus,
            driver=self.driver,
            departure_time=timezone.now() + timezone.timedelta(hours=5),
            arrival_time=timezone.now() + timezone.timedelta(hours=8)
        ).full_clean()

        # Creating a BusShift earlier with the same bus and driver should not be an issue
        BusShiftFactory.create(
            bus=self.bus,
            driver=self.driver,
            departure_time=timezone.now(),
            arrival_time=timezone.now() + timezone.timedelta(hours=3)
        ).full_clean()

        # CASE 2: A Bus shift that starts earlier exists but the arrival time is before the new departure time
        BusShift.objects.all().delete()
        BusShiftFactory.create(
            bus=self.bus,
            driver=self.driver,
            departure_time=timezone.now(),
            arrival_time=timezone.now() + timezone.timedelta(hours=3)
        ).full_clean()

        # Creating a BusShift in the future should not be an issue
        BusShiftFactory.create(
            bus=self.bus,
            driver=self.driver,
            departure_time=timezone.now() + timezone.timedelta(hours=4),
            arrival_time=timezone.now() + timezone.timedelta(hours=8)
        ).full_clean()

        # CASE 3: Complete overlapping arrival time and departure time
        BusShift.objects.all().delete()
        BusShiftFactory.create(
            bus=self.bus,
            driver=self.driver,
            departure_time=timezone.now() + timezone.timedelta(hours=1),
            arrival_time=timezone.now() + timezone.timedelta(hours=4)
        ).full_clean()

        # BusShift whose departure time and arrival time are completely within the existing one should not be possible
        with self.assertRaises(ValidationError):
            # Create a new shift for a different driver, but same bus
            BusShiftFactory.create(
                bus=self.bus,
                departure_time=timezone.now() + timezone.timedelta(hours=2),
                arrival_time=timezone.now() + timezone.timedelta(hours=3)
            ).full_clean()

        # However, if this is not for the same bus or driver, no issue
        BusShiftFactory.create(
            departure_time=timezone.now() + timezone.timedelta(hours=2),
            arrival_time=timezone.now() + timezone.timedelta(hours=3)
        ).full_clean()

        # CASE 4: Overlapping departure time but arrival time is after
        BusShift.objects.all().delete()
        BusShiftFactory.create(
            bus=self.bus,
            driver=self.driver,
            departure_time=timezone.now() + timezone.timedelta(hours=1),
            arrival_time=timezone.now() + timezone.timedelta(hours=4)
        ).full_clean()

        with self.assertRaises(ValidationError):
            # Create a new shift for same driver (but different bus)
            # departure time is before the arrival time of the existing BusShift
            BusShiftFactory.create(
                driver=self.driver,
                departure_time=timezone.now() + timezone.timedelta(hours=2),
                arrival_time=timezone.now() + timezone.timedelta(hours=8)
            ).full_clean()

        # CASE 5: Overlapping arrival time but departure time is before
        BusShift.objects.all().delete()
        BusShiftFactory.create(
            bus=self.bus,
            driver=self.driver,
            departure_time=timezone.now() + timezone.timedelta(hours=2),
            arrival_time=timezone.now() + timezone.timedelta(hours=4)
        ).full_clean()

        with self.assertRaises(ValidationError):
            # departure time is earlier but arrival time is between departure and arrival of the existing BusShift
            BusShiftFactory.create(
                driver=self.driver,
                bus=self.bus,
                departure_time=timezone.now() + timezone.timedelta(hours=1),
                arrival_time=timezone.now() + timezone.timedelta(hours=3)
            ).full_clean()

        # CASE 6: Complete overlapping of both arrival time and departure time
        BusShift.objects.all().delete()
        BusShiftFactory.create(
            bus=self.bus,
            driver=self.driver,
            departure_time=timezone.now() + timezone.timedelta(hours=2),
            arrival_time=timezone.now() + timezone.timedelta(hours=4)
        ).full_clean()

        with self.assertRaises(ValidationError):
            # departure time earlier and arrival time is after
            BusShiftFactory.create(
                driver=self.driver,
                bus=self.bus,
                departure_time=timezone.now() + timezone.timedelta(hours=1),
                arrival_time=timezone.now() + timezone.timedelta(hours=8)
            ).full_clean()

