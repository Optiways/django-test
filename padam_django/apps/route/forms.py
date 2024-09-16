from django import forms
from .models import BusShift
from django.core.exceptions import ValidationError

class BusShiftForm(forms.ModelForm):
    """
        This form makes possible to clean steps bus stop
    """
    class Meta:
        model = BusShift
        fields = '__all__'

    def clean(self):
        """
            Check that all steps times are between starting and ending times
        """
        start = self.cleaned_data.get('start')
        end = self.cleaned_data.get('end')
        steps = self.cleaned_data.get('steps')
        if steps:
            for step in steps:
                if step.time > end.time or step.time < start.time:
                    raise ValidationError(
                        {"steps": "Steps must be later than starting bus time and before ending bus stop time"}
                    )
        return self.cleaned_data