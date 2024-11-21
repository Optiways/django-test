import re
from django import forms
from padam_django.apps.schedules.models import BusShift, BusStop


class BusShiftForm(forms.ModelForm):
    class Meta:
        model = BusShift
        fields = ["driver", "bus"]

    def clean(self):
        start = min(
            [
                v
                for k, v in self.data.items()
                if re.match("busstop_set-[0-9]+-stoptime", k) and v
            ]
        )
        end = max(
            [
                v
                for k, v in self.data.items()
                if re.match("busstop_set-[0-9]+-stoptime", k) and v
            ]
        )
        if not BusShift(
            bus=self.cleaned_data["bus"], driver=self.cleaned_data["driver"]
        ).shift_is_available(start, end):
            raise forms.ValidationError(
                "Shift is not available, it collides with another shift"
            )
        return super().clean()
