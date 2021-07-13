from padam_django.apps.common.management.base import CreateDataBaseCommand

from padam_django.apps.fleet.factories import BusFactory


class Command(CreateDataBaseCommand):

    help = 'Create few buses'

    def handle(self, *args, **options):
        super().handle(*args, **options)
        self.stdout.write(f'Creating {self.number} buses ...')
        BusFactory.create_batch(size=self.number)
