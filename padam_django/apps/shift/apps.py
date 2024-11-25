from django.apps import AppConfig


class ShiftConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "padam_django.apps.shift"

    def ready(self):
        import padam_django.apps.shift.receivers  # noqa
