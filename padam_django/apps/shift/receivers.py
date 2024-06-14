from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import BusShift, ScheduleStop


@receiver(post_save, sender=ScheduleStop)
def update_bus_shift_departure_or_arrival(sender, instance, **kwargs):
    bus_shift = BusShift.objects.get(id=instance.bus_shift.id)

    if bus_shift.first_stop is None and bus_shift.last_stop is None:
        bus_shift.first_stop = instance.arrival
        bus_shift.last_stop = instance.arrival
        bus_shift.save()

    if instance.arrival < bus_shift.first_stop:
        bus_shift.first_stop = instance.arrival
        bus_shift.save()
    if instance.arrival > bus_shift.last_stop:
        bus_shift.last_stop = instance.arrival
        bus_shift.save()
