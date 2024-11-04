from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from .models import BusShift


class BusShiftForm(forms.ModelForm):
    """
    A Django form for creating or updating `BusShift` instances, which represent
    individual bus shifts that must contain a unique sequence of at least two bus stops.

    This form performs validation on the set of bus stops provided to ensure:
    - No duplicate stops are included within the shift.
    - At least two unique bus stops are specified for a valid shift.

    Attributes:
        model: The model associated with this form, set to `BusShift`.
        fields: Specifies that all fields in `BusShift` should be included in the form.
    """

    class Meta:
        model = BusShift
        fields = "__all__"

    def clean(self):
        """
        Override the clean method to perform custom validation on bus stops.

        This method checks:
        - No duplicate bus stops are included in the shift.
        - At least two unique bus stops are specified.

        Raises:
            ValidationError: If duplicate stops are found or fewer than two unique stops are provided.

        Returns:
            cleaned_data: The validated form data.
        """
        cleaned_data = super().clean()
        stops = self.cleaned_data.get("stops")

        if stops:
            unique_stops = set()
            for stop in stops:
                unique_stops.add(stop)

            if len(unique_stops) < 2:
                raise ValidationError("At least two bus stops are required.")

            self._calculate_shift_times(unique_stops)
        self._validate_unique_shift()
        return cleaned_data

    def _calculate_shift_times(self, unique_stops):
        """
        Calculate start_time, end_time, and duration based on unique bus stops.
        Assigns None values if no stops are assigned, and duration as zero.
        """
        if unique_stops:
            sorted_stops = sorted(unique_stops, key=lambda x: x.stop_time)
            first_stop = sorted_stops[0]
            last_stop = sorted_stops[-1]

            self.instance.start_time = first_stop.stop_time
            self.instance.end_time = last_stop.stop_time
        else:
            self.instance.start_time = self.instance.end_time = None

    def _validate_unique_shift(self):
        """
        Ensure there are no overlapping shifts for the same bus or driver.

        Raises:
            ValidationError: If any overlap exists with another shift's start or end times.
        """

        if not self.instance.start_time or not self.instance.end_time:
            return

        bus = self.cleaned_data.get("bus")
        driver = self.cleaned_data.get("driver")
        if bus and driver and self.instance.start_time and self.instance.end_time:
            overlapping_shifts = BusShift.objects.exclude(pk=self.instance.pk).filter(
                Q(bus=bus) | Q(driver=driver),
                Q(start_time__lt=self.instance.end_time),
                Q(end_time__gt=self.instance.start_time),
            )
        if overlapping_shifts.exists():
            raise ValidationError(
                "This shift overlaps with an existing shift for the same bus or driver."
            )
