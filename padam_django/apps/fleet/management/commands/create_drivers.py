from padam_django.apps.common.management.base import CreateDataBaseCommand

from padam_django.apps.fleet.factories import DriverFactory


class Command(CreateDataBaseCommand):

    help = 'Create few drivers'

    def handle(self, *args, **options):
        super().handle(*args, **options)
        self.stdout.write(f'Creating {self.number} drivers ...')
        DriverFactory.create_batch(size=self.number)
