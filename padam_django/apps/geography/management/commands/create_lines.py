from padam_django.apps.common.management.base import CreateDataBaseCommand

from padam_django.apps.geography.factories import BusLineWith5StopFactory


class Command(CreateDataBaseCommand):

    help = 'Create few lines'

    def handle(self, *args, **options):
        super().handle(*args, **options)
        self.stdout.write(f'Creating {self.number} lines ...')
        BusLineWith5StopFactory.create_batch(size=self.number)
