from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from padam_django.apps.fleet.models import BusShift
import logging

logger = logging.getLogger("Django Signals")


@receiver(m2m_changed, sender=BusShift.stops.through)
def update_shift_times(sender, instance, action, **kwargs):
    """Compute departure_time and arrival_time when a bus stop is added
    N.B: Stops are already ordered by departure time
    TODO: Implement logger config in settings to handle logs
    """
    logger.info("update_shift_times signal called")
    if action in ["post_add", "post_remove", "post_clear"]:
        # Get all the stops in the current shift
        stops = instance.stops

        if stops.exists():
            instance.departure_time = stops.first().departure_time
            instance.arrival_time = stops.last().departure_time
            instance.save()
