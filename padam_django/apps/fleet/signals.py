from django.db.models.signals import (
    m2m_changed,
    post_save
)
from django.dispatch import receiver

from .models import BusShift


# Constraints on the Bus Stops
@receiver(m2m_changed, sender = BusShift.bus_stops.through)
def set_shift(sender, instance, action, **kwargs):


    '''
        Every time a bus shit object is changed, there will be a check on the m2m relation with
        Bus stop and check the first stop of the day to add it to the start of the shift.
        Post add method will be triggered only if the Bus Shift object M2M to BusStop is changed 
    '''
    if action == "post_add":
        """
            We want all the bus stops related to our bus shift ordered by the schedule time.
            After that we catch the first and the last element of the queryset to set our start and 
            end shift
        """
        bus_stop_schedule =  instance.bus_stops.all().order_by('schedule')
        instance.start_shift = bus_stop_schedule.first().schedule
        instance.end_shift = bus_stop_schedule.last().schedule
        instance.save()



@receiver(m2m_changed, sender = BusShift.bus_stops.through)
def prevent_less_2_m2m(sender, instance, action, **kwargs):

    """
        We raise an exception if the shift don't have 2 or more stops
    """
    if action == "post_add":
        if instance.bus_stops.all().count() <= 1:
            raise Exception(
                    f'You need at least two stop to create the shift'
            )
            
