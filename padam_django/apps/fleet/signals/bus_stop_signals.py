from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from padam_django.apps.fleet.models import BusStop


@receiver(post_delete, sender=BusStop)
@receiver(post_save, sender=BusStop)
def update_linked_shift(sender, instance: BusStop, using, **kwargs):
    instance.shift.update_on_linked_stop_change()
