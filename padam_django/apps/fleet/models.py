from django.db import models
from padam_django.apps.common.utils import period_overlap
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Driver(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='driver')

    def __str__(self):
        return f"Driver: {self.user.username} (id: {self.pk})"


class Bus(models.Model):
    licence_plate = models.CharField("Name of the bus", max_length=10)

    class Meta:
        verbose_name_plural = "Buses"

    def __str__(self):
        return f"Bus: {self.licence_plate} (id: {self.pk})"


class BusShift(models.Model):
    bus = models.ForeignKey(Bus, null=True, on_delete=models.SET_NULL)
    driver = models.ForeignKey(Driver, null=True, on_delete=models.SET_NULL)
    line = models.ForeignKey('geography.BusLine', null=True, on_delete=models.SET_NULL)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    
    def check_availability_for_entity(self, entity):
        """Takes an entity (example: {'driver': driver_object}).
            Raises a ValidationError if the entity is not available for this shift"""
        start = self.departure_time
        end = self.arrival_time
        other_shifts_taken_by_entity = BusShift.objects.filter(**entity).exclude(pk=self.pk).all()
        for shift in other_shifts_taken_by_entity:
            if period_overlap(shift.departure_time, shift.arrival_time, start, end):
                entity_type = list(entity.keys())[0]
                raise ValidationError(
                    _(f"The {entity_type} already is on another shift (line: {shift.line}, departure: {shift.departure_time}, arrival: {shift.arrival_time})"),
                    code="taken_" + entity_type)
    
    def clean(self):
        start = self.departure_time
        end = self.arrival_time
        if start and end and start > end:
            raise ValidationError(
                    _(f"The departure time {start} must be inferior to the arrival time {end}.)"),
                    code="departure_time_inferior_to_arrival_time")
        self.check_availability_for_entity({'driver': self.driver})
        self.check_availability_for_entity({'bus': self.bus})

    class Meta:
        verbose_name_plural = "Bus shifts"
    
    def __str__(self):
        return f"Bus: {self.bus.licence_plate} - Driver: {self.driver.user} (id: {self.pk})"
