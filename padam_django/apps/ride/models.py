from django.db import models
import uuid as uuid_util
from django.utils.datetime_safe import datetime
from padam_django.apps.geography.models import Place
from padam_django.apps.fleet.models import Driver, Bus


class CustomManager(models.Manager):
    pass


class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid_util.uuid4)
    created_at = models.DateTimeField(default=datetime.now)
    deleted = models.BooleanField(default=False)

    objects = CustomManager()

    class Meta:
        abstract = True

    abstract = True

    def delete(self, **kwargs):
        self.deleted = True
        self.save()


class BusStop(BaseModel):
    stop_location = models.OneToOneField(Place, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return f"{self.stop_location} (uuid: {self.uuid})"


class BusShift(BaseModel):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, null=False, blank=False)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=False, blank=False)
    bus_stops = models.ManyToManyField(BusStop, through="BusSubRoute")
    departure_time = models.DateTimeField(default=None, null=True)
    arrival_time = models.DateTimeField(default=None, null=True)
    is_completed = models.BooleanField(default=False)  # True if number of stop > 2, else False

    def set_departure_time(self):
        departure_time = BusSubRoute.objects.filter(
            bus_shift__uuid=self.uuid,
            deleted=False). \
            order_by("passage_datetime").values("passage_datetime").first()["passage_datetime"]
        self.departure_time = departure_time
        self.save()

    def set_arrival_time(self):
        arrival_time = BusSubRoute.objects.filter(
            bus_shift__uuid=self.uuid,
            deleted=False). \
            order_by("-passage_datetime").values("passage_datetime").first()["passage_datetime"]
        self.arrival_time = arrival_time
        self.save()

    def get_shift_duration(self):
        shift_duration = self.arrival_time - self.departure_time
        return shift_duration

    def get_number_of_stop(self):
        number_of_stop = BusSubRoute.objects.filter(
            bus_shift__uuid=self.uuid,
            deleted=False).count()
        return number_of_stop

    def set_is_completed(self):
        if self.get_number_of_stop() >= 2:
            self.is_completed = True
            self.save()

    def __str__(self):
        return f"{self.bus} {self.driver} (uuid: {self.uuid})"


class BusSubRoute(BaseModel):
    bus_stop = models.ForeignKey(BusStop, on_delete=models.CASCADE, null=False, blank=False)
    bus_shift = models.ForeignKey(BusShift, on_delete=models.CASCADE, null=False, blank=False)
    passage_datetime = models.DateTimeField(null=False, blank=False)

    def __str__(self):
        return f"{self.bus_shift} - {self.bus_stop} - {self.passage_datetime}"
