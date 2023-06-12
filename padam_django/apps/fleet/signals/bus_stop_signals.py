from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from padam_django.apps.fleet.models import BusStop
from padam_django.apps.fleet.exceptions import (
    DriverOtherShiftsOverlapException,
    BusOtherShiftsOverlapException,
    StopWouldOverlapBusOtherShifts,
    StopWouldOverlapDriverOtherShifts,
)


@receiver(post_delete, sender=BusStop)
@receiver(post_save, sender=BusStop)
def update_linked_shift(sender, instance: BusStop, using, **kwargs):
    try:
        instance.shift.save()
    except DriverOtherShiftsOverlapException:
        raise StopWouldOverlapDriverOtherShifts(
            f"Can't set stop {instance.pk} to {instance.datetime}. Would overlap driver's other shifts."
        )
    except BusOtherShiftsOverlapException:
        raise StopWouldOverlapBusOtherShifts(
            f"Can't set stop {instance.pk} to {instance.datetime}. Would overlap bus's other shifts."
        )
    return
