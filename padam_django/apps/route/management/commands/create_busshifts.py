from padam_django.apps.common.management.base import CreateDataBaseCommand
from padam_django.apps.route.factories import BusShiftFactory, BusStopFactory


class Command(CreateDataBaseCommand):
    """
    Create bus shifts with BusStops using the CreateDataBaseCommand.

    This command creates a specified number of bus shifts with two BusStops each.
    The number of bus shifts to be created can be specified using the '--number' option.
    """

    help = 'Create bus shifts with BusStops'

    def handle(self, *args, **options):
        """
        Handle the execution of the command.

        This method creates the specified number of bus shifts with two BusStops each,
        using the CreateDataBaseCommand's handle method. It also prints the progress
        and completion messages to the console.
        """
        super().handle(*args, **options)
        for _ in range(self.number):
            stops = BusStopFactory.create_batch(2)
            shift = BusShiftFactory()
            shift.stops.set(stops)
            shift.save()
            self.stdout.write(f'Created BusShift {shift.pk} with {len(stops)} stops')
