from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    @property
    def is_driver(self) -> bool:
        """Define if the user is related to a driver."""
        return hasattr(self, 'driver')
