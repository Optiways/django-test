from io import StringIO
from django.test import TestCase

from django.core.management import call_command
from padam_django.apps.fleet.models import BusStop


class TestCreateBusStopsCommand(TestCase):
    def test_create_bus_stops(self):
        # Arrange
        output = StringIO()
        number_of_bus_stops = 5

        # Ensure no bus stop exists in DB
        self.assertEqual(BusStop.objects.count(), 0)

        # Act
        call_command("create_bus_stops", number=number_of_bus_stops, stdout=output)

        # Assert
        self.assertIn(f"Creating {number_of_bus_stops} bus stops ...", output.getvalue())
        self.assertEqual(BusStop.objects.count(), number_of_bus_stops)
