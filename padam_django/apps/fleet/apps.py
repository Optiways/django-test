from django.apps import AppConfig


class FleetConfig(AppConfig):
    name = "padam_django.apps.fleet"

    def ready(self):
        import padam_django.apps.fleet.signals
