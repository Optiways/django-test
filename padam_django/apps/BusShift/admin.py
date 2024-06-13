from django.contrib import admin

from padam_django.apps.BusShift.models import BusShift


@admin.register(BusShift)
class BusShiftAdmin(admin.ModelAdmin):
    list_display = ('bus', 'driver',
                    'shift_start', 'shift_end', 'duration')
    filter_horizontal = ('places',)
    search_fields = ('BusShiftname', 'bus__name', 'driver__name')

    def duration(self, obj):
        return obj.duration
