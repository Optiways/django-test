from django.contrib import admin

from padam_django.apps.fleet import models
from padam_django.apps.fleet.admin.formsets import ScheduledStopInlineFormSet


class ScheduledStopInlineAdmin(admin.TabularInline):
    formset = ScheduledStopInlineFormSet
    model = models.BusShiftScheduledStop
    min_num = 2

    def get_formset(self, request, obj=None, **kwargs):
        kwargs.update(validate_min=True)
        return super().get_formset(request, obj, **kwargs)
