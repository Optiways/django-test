from django.db import models


class Driver(models.Model):
    user = models.OneToOneField(
        "users.User", on_delete=models.CASCADE, related_name="driver"
    )

    def __str__(self):
        return f"Driver: {self.user.username} (id: {self.pk})"
