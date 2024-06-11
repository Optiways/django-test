from padam_django.apps.common.management.base import CreateDataBaseCommand

from padam_django.apps.geography.factories import BusStopFactory


class Command(CreateDataBaseCommand):

    help = 'Create few stops'

    def handle(self, *args, **options):
        super().handle(*args, **options)
        self.stdout.write(f'Creating {self.number} stops ...')
        BusStopFactory.create_batch(size=self.number)
