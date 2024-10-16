from padam_django.apps.common.management.base import CreateDataBaseCommand

from padam_django.apps.fleet.factories import BusStopFactory


class Command(CreateDataBaseCommand):
    help = "Create few bus stops"

    def handle(self, *args, **options):
        super().handle(*args, **options)
        self.stdout.write(f"Creating {self.number} bus stops ...")
        BusStopFactory.create_batch(size=self.number)
