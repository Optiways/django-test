from django import forms
from django.core.exceptions import ValidationError


class ScheduledStopInlineFormSet(forms.models.BaseInlineFormSet):
    def clean(self):
        super().clean()

        # Validate non-overlapping shift schedule for current instance driver and bus
        times = [
            form.cleaned_data["time"]
            for form in self.forms
            if form.cleaned_data.get("time", None)
        ]

        if times and len(times) >= 2:
            departure = min(times)
            arrival = max(times)

            if (
                self.instance.driver
                and self.instance.driver.shifts.exclude(pk=self.instance.pk)
                .overlapping(departure, arrival)
                .exists()
            ):
                raise ValidationError(
                    "The selected driver already has a shift overlapping this one"
                )

            if (
                self.instance.bus
                and self.instance.bus.shifts.exclude(pk=self.instance.pk)
                .overlapping(departure, arrival)
                .exists()
            ):
                raise ValidationError(
                    "The selected bus already has a shift overlapping this one"
                )
