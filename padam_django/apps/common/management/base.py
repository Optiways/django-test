from django.core.management.base import BaseCommand


class CreateDataBaseCommand(BaseCommand):

    def __init__(self, *args, **kwargs):
        self.number = None
        super().__init__(*args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument(
            '--number',
            '-n',
            dest='number',
            default=5,
            type=int,
            help='Specify the number of items to create',
        )

    def _init_options(self, **options):
        self.number = options['number']

    def handle(self, *args, **options):
        self._init_options(**options)
