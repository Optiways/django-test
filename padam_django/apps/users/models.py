from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    
    @property
    def is_driver(self) -> bool:
        """Define if the user is related to a driver."""
        return hasattr(self, 'driver')
