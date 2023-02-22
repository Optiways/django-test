from datetime import time
from django.test import TestCase

from padam_django.apps.fleet.factories import BusShiftFactory, DriverFactory
from padam_django.apps.fleet.services import check_driver_availability


class TestDriverAvailabilityModel(TestCase):
    def setUp(self) -> None:
        departure_time = time(hour=8, minute=0)
        arrival_time = time(hour=10, minute=0)
        self.driver = DriverFactory()
        BusShiftFactory(
            driver=self.driver, departure_time=departure_time, arrival_time=arrival_time
        )

    def test_driver_availability_when_shift_is_overlapping_departure_time(self):
        # Arrange
        departure_time = time(hour=7, minute=0)
        arrival_time = time(hour=9, minute=0)

        # Act
        is_driver_available = check_driver_availability(self.driver, departure_time, arrival_time)

        # Assert
        self.assertFalse(is_driver_available)

    def test_driver_availability_when_shift_is_not_overlapping_departure_time(self):
        departure_time = time(hour=7, minute=0)
        arrival_time = time(hour=7, minute=30)

        is_driver_available = check_driver_availability(self.driver, departure_time, arrival_time)

        self.assertTrue(is_driver_available)

    def test_driver_availability_when_shift_is_overlapping_arrival_time(self):
        # Arrange
        departure_time = time(hour=9, minute=0)
        arrival_time = time(hour=11, minute=0)

        # Act
        is_driver_available = check_driver_availability(self.driver, departure_time, arrival_time)

        # Assert
        self.assertFalse(is_driver_available)

    def test_driver_availability_when_shift_is_not_overlapping_arrival_time(self):
        departure_time = time(hour=10, minute=30)
        arrival_time = time(hour=11, minute=0)

        is_driver_available = check_driver_availability(self.driver, departure_time, arrival_time)

        self.assertTrue(is_driver_available)

    def test_driver_availability_when_shift_is_inner_departure_and_arrival(self):
        departure_time = time(hour=9, minute=0)
        arrival_time = time(hour=9, minute=30)

        is_driver_available = check_driver_availability(self.driver, departure_time, arrival_time)

        self.assertFalse(is_driver_available)

    def test_driver_availability_when_shift_is_outer_including_departure_and_arrival(self):
        departure_time = time(hour=7, minute=30)
        arrival_time = time(hour=11, minute=30)

        is_driver_available = check_driver_availability(self.driver, departure_time, arrival_time)

        self.assertFalse(is_driver_available)
