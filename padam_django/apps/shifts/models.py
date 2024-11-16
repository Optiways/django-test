from typing import Iterable, Union
from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime


def fmt_date_time(date_time: datetime):
    return date_time.strftime("%d/%m/%Y à %H:%M")


class BusStop(models.Model):
    place = models.OneToOneField("geography.Place", on_delete=models.CASCADE)
    date_time = models.DateTimeField()

    def __str__(self):
        # TODO: Format date time to be human-readable
        return (
            f"BusStop: '{self.place.name}' [{fmt_date_time(self.date_time)}] "
            f"(id: {self.pk})"
        )


class BusShift(models.Model):
    bus = models.ForeignKey(
        "fleet.Bus", null=True, blank=True, on_delete=models.CASCADE
    )
    driver = models.ForeignKey(
        "fleet.Driver", null=True, blank=True, on_delete=models.CASCADE
    )
    # TODO: Order by date_time to avoid doing so in other places
    stops = models.ManyToManyField(BusStop)

    @property
    def first_stop(self):
        return self.stops.all().order_by("date_time").first()

    @property
    def first_stop_date_time(self):
        return self.first_stop.date_time if self.first_stop else None

    @property
    def last_stop(self):
        return self.stops.all().order_by("date_time").last()

    @property
    def stops_count(self):
        return len(self.stops.all())

    def validate(self):
        # TODO: Mutualize validation from BusShiftAdminForm + add check that both Bus and Driver are set
        # Skip validation if the object is not saved yet (no primary key)
        if not self.pk:
            return

    @property
    def is_valid(self) -> bool:
        """Check that the BusShift is fully ready (does not violate
        constraints and has both a Driver and a Bus assigned to.

        Returns:
            bool: Validity status
        """
        try:
            self.validate()
        except ValidationError:
            return False
        return True

    def clean(self) -> None:
        try:
            self.validate()
        except ValidationError as e:
            raise (e)

    def save(
        self,
        force_insert: bool = False,
        force_update: bool = False,
        using: Union[str, None] = None,
        update_fields: Union[Iterable[str], None] = None,
    ) -> None:
        # Calling clean to validate data before saving
        self.full_clean()
        return super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        bus_license_plate = self.bus.licence_plate if self.bus else "<NO BUS>"
        driver_first_name = (
            self.driver.user.first_name if self.driver else "<NO DRIVER>"
        )
        driver_last_name = self.driver.user.last_name if self.driver else ""
        return (
            f"BusShift: {bus_license_plate} "
            f"[{fmt_date_time(self.first_stop.date_time)} - "
            f"{fmt_date_time(self.last_stop.date_time)}] "
            f"conducted by {driver_first_name} {driver_last_name} "
            f"(id: {self.pk})"
        )
