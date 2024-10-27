from django.core.exceptions import ValidationError
from django.db import models

from padam_django.apps.common.models import TsCreateUpdateMixin
from padam_django.apps.common.validators import validate_future_date


class BusStop(TsCreateUpdateMixin):
    """
    Base class for the BusStop models.

    The user must only fill the following fields:
        - place: select where the user will be picked up
        - ts_requested: select at what time the user should be picked up

    The other fields are for object usage monitoring:
        - ts_create
        - ts_update

    For feedback with the BusShift algorithm:
        - ts_estimated
        - ts_boarded
        - has_boarded
    """

    place = models.ForeignKey("geography.Place", on_delete=models.CASCADE)
    ts_requested = models.DateTimeField(
        verbose_name="Requested boarding time",
        help_text="Requested time by the user to get picked up",
        blank=False,
        null=False,
        validators=[validate_future_date],
    )

    # The following fields are not user inputs
    ts_estimated = models.DateTimeField(
        verbose_name="Estimated boarding time",
        help_text="Estimated Bus arrival time by the BusShift algorithm",
        blank=True,
        null=True,
    )
    ts_boarded = models.DateTimeField(
        verbose_name="Real boarding time",
        help_text="Time when the user has been picked up by the bus",
        blank=True,
        null=True,
    )
    has_boarded = models.BooleanField(
        verbose_name="Has Boarded",
        help_text="Checks if the user has boarded the bus",
        default=False,
    )
    # TODO: In a later version, allow cancellation of BusStop for soft deletion

    class Meta:
        abstract = True

    def __str__(self):
        return f"User: {self.user.username}, Place: {self.place.name}, Time: {self.ts_requested.isoformat()} (id: {self.pk})"

    def _get_start_pk(self):
        raise NotImplementedError

    def _clean_overlapping_itinerary(self):
        """
        Checks if a created itinerary doesn't overlap with another one.
        """
        itinerary_qs = self.user.start_bus_stops.select_related(
            "end_bus_stops"
        ).exclude(end_bus_stops__isnull=True)
        if self.pk:
            itinerary_qs = itinerary_qs.exclude(pk=self._get_start_pk())

        itinerary_list = itinerary_qs.values_list(
            "ts_requested", "end_bus_stops__ts_requested"
        )
        for i in itinerary_list:
            ts_start = i[0]
            ts_end = i[1]
            if ts_start <= self.ts_requested and self.ts_requested <= ts_end:
                raise ValidationError(
                    {
                        "ts_requested": f"Can't start an itinerary because one is already planned for this time period: {ts_start.isoformat()} -> {ts_end.isoformat()}",
                    }
                )

    def clean(self):
        super().clean()
        self._clean_overlapping_itinerary()


class StartBusStop(BusStop):
    """
    The user must first create a `StartBusStop` and then assign an `EndBusStop` to it
    if he wants it to be taken into account into the BusShift algorithm.
    """

    user = models.ForeignKey(
        "users.User",
        verbose_name="User",
        help_text="User that booked a bus",
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = (("user", "place", "ts_requested"),)
        default_related_name = "start_bus_stops"
        abstract = False

    @property
    def has_end(self) -> bool:
        """Define if the BusStop has an end."""
        return hasattr(self, "end")

    def _get_start_pk(self):
        return self.pk


class EndBusStop(BusStop):
    """
    A start and an end `BusStop` have a One to One relationship. The pair form an itinerary.
    """

    start = models.OneToOneField(
        "travel.StartBusStop",
        verbose_name="Starting BusStop",
        help_text="Starting BusStop that will form an itinerary",
        on_delete=models.CASCADE,
    )
    shift = models.ForeignKey(
        "travel.BusShift",
        verbose_name="Bus shift",
        help_text="Bus shift that will handle these stops",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        default_related_name = "end_bus_stops"
        abstract = False

    @property
    def user(self):
        return self.start.user

    def clean(self):
        super().clean()
        start = self.start

        start_place = start.place
        if self.place == start_place:
            raise ValidationError(
                {
                    "place": f"The itinerary is a round trip: {self.place.name} -> {start_place}",
                }
            )

        start_requested = start.ts_requested
        if self.ts_requested <= start_requested:
            raise ValidationError(
                {
                    "ts_requested": f"The end date of the itinerary {self.ts_requested.isoformat()} can't be before the start date of the itinerary {start_requested.isoformat()}",
                }
            )

    def _get_start_pk(self):
        return self.start.pk


class BusShift(models.Model):
    driver = models.ForeignKey(
        "fleet.Driver",
        verbose_name="Bus driver",
        help_text="Driver for this shift",
        on_delete=models.CASCADE,
    )
    bus = models.ForeignKey(
        "fleet.Bus",
        verbose_name="Bus",
        help_text="Bus for this shift",
        on_delete=models.CASCADE,
    )

    class Meta:
        default_related_name = "shifts"

    def __str__(self):
        return f"Driver: {self.driver.user.name}, Bus: {self.bus.licence_plate} (id: {self.pk})"

    def _get_stops(self):
        return self.end_bus_stops.select_related("start_bus_stops")

    def _get_shift_boundaries(self):
        return self._get_stops().aggregate(
            start=models.Min("start_bus_stops__ts_requested"),
            end=models.Max("ts_requested"),
        )

    @property
    def shift_start(self):
        return self._get_shift_boundaries()["start"]

    @property
    def shift_end(self):
        return self._get_shift_boundaries()["end"]

    @property
    def shift_duration(self):
        boundary = self._get_shift_boundaries()
        return boundary["end"] - boundary["start"]

    def _clean_object_available(self, obj, shift_boundary, field_name):
        def raise_error_message(start, end):
            raise ValidationError(
                {
                    field_name: f"The {field_name} is already booked for the period {start.isoformat()} -> {end.isoformat()}"
                }
            )

        current_shift_start = shift_boundary["start"]
        current_shift_end = shift_boundary["end"]

        shifts_qs = obj.shifts.prefetch_related(
            "end_bus_stops", "end_bus_stops__start_bus_stops"
        )
        if self.pk:
            shifts_qs = shifts_qs.exclude(pk=self.pk)
        shift_list = shifts_qs.values("pk").annotate(
            start=models.Min("end_bus_stops__start_bus_stops__ts_requested"),
            end=models.Max("end_bus_stops__ts_requested"),
        )
        for s in shift_list:
            shift_start = s["start"]
            shift_end = s["end"]
            if (
                (shift_start <= current_shift_end <= shift_end)
                or (shift_start <= current_shift_start <= shift_end)
                or (
                    current_shift_start <= shift_start
                    and shift_end <= current_shift_end
                )
            ):
                raise_error_message(shift_start, shift_end)

    def _clean_bus(self, shift_boundary):
        self._clean_object_available(
            self.bus,
            shift_boundary,
            field_name="bus",
        )

    def _clean_driver(self, shift_boundary):
        self._clean_object_available(self.driver, shift_boundary, field_name="driver")

    def clean(self):
        """
        The check for existing stops will be done on the form side
        """
        super().clean()
        shift_boundary = self._get_shift_boundaries()
        self._clean_bus(shift_boundary)
        self._clean_driver(shift_boundary)
