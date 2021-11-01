from padam_django.apps.common.management.base import CreateDataBaseCommand

from padam_django.apps.geography.factories import PlaceFactory


class Command(CreateDataBaseCommand):

    help = "Create few places"

    def handle(self, *args, **options):
        super().handle(*args, **options)
        self.stdout.write(f"Creating {self.number} places ...")
        PlaceFactory.create_batch(size=self.number)
