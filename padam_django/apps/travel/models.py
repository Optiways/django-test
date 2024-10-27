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


class StartBusStop(BusStop):
    """
    The user must first create a `StartBusStop` and then assign an `EndBusStop` to it
    if he wants it to be taken into account into the BusShift algorithm.
    """

    user = models.ForeignKey("users.User", on_delete=models.CASCADE)

    class Meta:
        unique_together = (("user", "place", "ts_requested"),)
        abstract = False

    @property
    def has_end(self) -> bool:
        """Define if the BusStop has an end."""
        return hasattr(self, "end")


class EndBusStop(BusStop):
    """
    A start and an end `BusStop` have a One to One relationship. The pair form an itinerary.
    """

    start = models.OneToOneField(
        "travel.StartBusStop", on_delete=models.CASCADE, related_name="end"
    )

    class Meta:
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
