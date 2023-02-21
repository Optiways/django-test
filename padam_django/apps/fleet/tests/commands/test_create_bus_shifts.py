from io import StringIO
from django.test import TestCase

from django.core.management import call_command
from padam_django.apps.fleet.models import BusShift


class TestCreateBusShiftCommand(TestCase):
    def test_create_bus_shifts(self):
        # Arrange
        output = StringIO()
        number_of_bus_shifts = 5

        # Ensure bus shift does not exist in db
        self.assertEqual(BusShift.objects.count(), 0)

        # Act
        call_command("create_bus_shifts", number=number_of_bus_shifts, stdout=output)

        # Assert
        self.assertIn(f"Creating {number_of_bus_shifts} bus shifts...", output.getvalue())
        self.assertEqual(BusShift.objects.count(), number_of_bus_shifts)