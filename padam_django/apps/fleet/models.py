from django.db import models


class Driver(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='driver')

    def __str__(self):
        return f"Driver: {self.user.username} (id: {self.pk})"

    def available_at(self, date):
        return not any(shift.departure <= date <= shift.arrival for shift in self.shifts.all())


class Bus(models.Model):
    licence_place = models.CharField("Name of the bus", max_length=10)

    class Meta:
        verbose_name_plural = "Buses"

    def __str__(self):
        return f"Bus: {self.licence_place} (id: {self.pk})"

    def available_at(self, date):
        return not any(shift.departure <= date <= shift.arrival for shift in self.shifts.all())