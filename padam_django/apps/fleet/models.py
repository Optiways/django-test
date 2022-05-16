from django.db import models


class MixinValidator:
    def available_at(self, date):
        if not any(shift.journey_duration == "not available" for shift in self.shift.all()):
            return not any(shift.departure <= date <= shift.arrival for shift in self.shift.all())
        else:
            return True  # case of zero stop attributed to a shift - you have to be able to modify it anyway


class Driver(models.Model, MixinValidator):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='driver')

    def __str__(self):
        return f"Driver: {self.user.username} (id: {self.pk})"


class Bus(models.Model, MixinValidator):
    licence_plate = models.CharField("Name of the bus", max_length=10)

    class Meta:
        verbose_name_plural = "Buses"

    def __str__(self):
        return f"Bus: {self.licence_plate} (id: {self.pk})"
