from padam_django.apps.common.management.base import CreateDataBaseCommand


class Command(CreateDataBaseCommand):

    help = 'Create few bus shifts'

    def handle(self, *args, **options):
        super().handle(*args, **options)
        self.stdout.write(f'Creating {self.number} bus shifts ...')
        # TODO create bus shifts using busshift factory
