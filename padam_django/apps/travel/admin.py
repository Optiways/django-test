import logging
from typing import Any
from django.shortcuts import redirect
from django.db import IntegrityError
from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from . import models


class BusStopInline(admin.StackedInline):
    '''Define the BusStop inline form.'''

    model: models.BusStop = models.BusStop


@admin.register(models.BusShift)
class BusShiftAdmin(admin.ModelAdmin):
    '''Define and register the BusShift form in the admin interface.'''

    inlines: list[BusStopInline] = [BusStopInline]

    def changeform_view(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        '''Overwrite the super().changeform_view(...) to handle IntegrityError
        and send its message to the client on a pretty message box instead
        of crashing the server.

        Args:
            request (HttpRequest): The client socket.

        Returns:
            HttpResponse: The server response.
        '''

        try:
            return super().changeform_view(request, *args, **kwargs)
        except IntegrityError as e:
            self.message_user(
                request, f'Error on object saving: {e}', level=logging.ERROR
            )
            return redirect(request.path)
