from __future__ import annotations
from datetime import datetime
from operator import attrgetter
from typing import Any
from django.db import models, IntegrityError
from padam_django.apps.fleet.models import Driver, Bus
from padam_django.apps.geography.models import Place


class BusShift(models.Model):
    '''The bus shift model definition.'''

    driver: models.ForeignKey = models.ForeignKey(
        Driver, on_delete=models.CASCADE
    )
    bus: models.ForeignKey = models.ForeignKey(Bus, on_delete=models.CASCADE)

    def __str__(self) -> str:
        '''Overwrite the __str__ magic method.

        Returns:
            str: The model string representation.
        '''

        return (
            f'BusShift: {self.driver.user.username}/'
            f'{self.bus.licence_plate} (id: {self.pk})'
        )


class BusStop(models.Model):
    '''The bus stop model definition.'''

    bus_shift: models.ForeignKey = models.ForeignKey(
        BusShift, on_delete=models.CASCADE
    )
    place: models.ForeignKey = models.ForeignKey(
        Place, on_delete=models.CASCADE
    )
    passage_time: models.DateTimeField = models.DateTimeField(
        'Datetime of the bus passage'
    )

    def save(self, *args: Any, **kwargs: Any) -> BusStop:
        '''Overwrite the super().save(...) method.
        Add integrity control for:
            - A scheduled driver cannot have a passage_time that interferes
                with an existing BusShift.
            - A scheduled bus cannot have a passage_time that interferes
                with an existing BusShift.

        Raises:
            IntegrityError: If any of these controls is not valid.

        Returns:
            BusStop: The created model.
        '''

        driver_schedules: dict[int, list[datetime]] = self._entity_schedules(
            'bus_shift__driver__user__username'
        )
        bus_schedules: dict[int, list[datetime]] = self._entity_schedules(
            'bus_shift__bus__licence_plate'
        )
        merged_schedules: list[list[datetime]] = list(
            driver_schedules.values()
        ) + list(bus_schedules.values())

        for start_time, arrival_time in merged_schedules:
            if start_time <= self.passage_time <= arrival_time:
                raise IntegrityError(
                    f'Passage time interferes with an existing bus shift.'
                )

        return super().save(*args, **kwargs)

    def _entity_schedules(
        self, entity_filter: str
    ) -> dict[int, list[datetime]]:
        '''Get the entity schedules based on the given passage_time date
        for the given entity.
        An entity is a driver or a bus.
        The data is structured as follow:
            {
                <bus_shift_id:int>: [
                    <start_time:datetime>,
                    <end_time:datetime>,
                ],
                ...
            }
        This data allow to check easily if the given passe_time does not
        interferes with an existed BusShift.

        Args:
            entity_filter (str): The entity model filter.
                Example:
                    entity_filter=bus_shift__driver__user__username
                    The driver's username of the given bus_shift if filtered.

        Returns:
            dict[int, list[datetime]]: The formated data structure that
                represent the entity schedules.
        '''

        shift_range: dict[int, list[datetime]] = {}
        filters: dict[str, Any] = {
            # Example: bus_shift__driver__user__username: self.bus_shift.driver.user.username
            entity_filter: attrgetter(entity_filter.replace('__', '.'))(self),
            'passage_time__year': self.passage_time.year,
            'passage_time__month': self.passage_time.month,
            'passage_time__day': self.passage_time.day,
        }
        stop_set: models.QuerySet = BusStop.objects.filter(**filters).order_by(
            'passage_time'
        )

        for stop in stop_set:
            if not stop.bus_shift.id in shift_range:
                shift_range[stop.bus_shift.id] = [
                    stop.passage_time,
                    stop.passage_time,
                ]
            else:
                shift_range[stop.bus_shift.id][1] = stop.passage_time

        return shift_range

    def __str__(self) -> str:
        '''Overwrite the __str__ magic method.

        Returns:
            str: The model string representation.
        '''

        return (
            f'BusStop: {self.bus_shift.pk}/{self.place.name} (id: {self.pk})'
        )
