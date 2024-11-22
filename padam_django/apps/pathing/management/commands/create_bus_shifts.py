from padam_django.apps.common.management.base import CreateDataBaseCommand

from padam_django.apps.pathing.factories.bus_shift_factory import BusShiftFactory

class Command(CreateDataBaseCommand):

    help = 'Create few bus shifts'

    def handle(self, *args, **options):
        super().handle(*args, **options)
        self.stdout.write(f'Creating {self.number} bus shifts ...')
        BusShiftFactory.create_batch(size=self.number)
