from django.db import models


class BusShift(models.Model):
    name = models.CharField("Name of the Busshift",
                            max_length=100, default="Test")

    class Meta:
        verbose_name_plural = "BusShift"

    def __str__(self):
        return f"BusShift: {self.name}"
