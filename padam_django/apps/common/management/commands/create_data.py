from django.core import management
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = 'Create test data'

    def handle(self, *args, **options):
        management.call_command('create_users', number=5)
        management.call_command('create_drivers', number=5)
        management.call_command('create_buses', number=10)
        management.call_command('create_places', number=30)
        management.call_command('create_bus_stops', number=100)
