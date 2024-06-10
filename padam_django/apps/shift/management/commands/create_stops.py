from padam_django.apps.common.management.base import CreateDataBaseCommand

from padam_django.apps.shift.factories import BusStopFactory


class Command(CreateDataBaseCommand):

    help = 'Create few Bus Stops'

    def handle(self, *args, **options):
        super().handle(*args, **options)
        self.stdout.write(f'Creating {self.number} bus stops ...')
        BusStopFactory.create_batch(size=self.number)
