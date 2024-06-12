from padam_django.apps.common.management.base import CreateDataBaseCommand

from padam_django.apps.BusShift.factories import BusShiftFactory


class Command(CreateDataBaseCommand):

    help = 'Create few shift'

    def handle(self, *args, **options):
        super().handle(*args, **options)
        self.stdout.write(f'Creating {self.number} shift ...')
        BusShiftFactory.create_batch(size=self.number)
