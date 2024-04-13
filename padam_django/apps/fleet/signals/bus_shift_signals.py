from django.db.models.signals import post_save
from django.dispatch import receiver

from padam_django.apps.fleet.models import BusShift
from padam_django.apps.fleet.exceptions import (
    DriverOtherShiftsOverlapException,
    BusOtherShiftsOverlapException,
)


@receiver(post_save, sender=BusShift)
def ensure_overlapping_is_fine(
    sender, instance: BusShift, using, update_fields, **kwargs
):
    if instance.bus_has_overlapping_shifts():
        raise BusOtherShiftsOverlapException(
            f"{instance.bus} can't be assigned to shift."
        )
    elif instance.driver_has_overlapping_shifts():
        raise DriverOtherShiftsOverlapException(
            f"{instance.driver} can't be assigned to shift."
        )
    else:
        return
