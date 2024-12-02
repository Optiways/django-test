from django.db import models


class Place(models.Model):
    name = models.CharField("Name of the place", max_length=50)

    longitude = models.DecimalField("Longitude", max_digits=9, decimal_places=6)
    latitude = models.DecimalField("Latitude", max_digits=9, decimal_places=6)

    class Meta:
        # Two places cannot be located at the same coordinates.
        unique_together = (("longitude", "latitude"), )

    def __str__(self):
        return f"Place: {self.name} (id: {self.pk})"
    
    class Meta:
        ordering = ['name']


class BusStop(models.Model):
    name = models.CharField("Name of the place", max_length=50)
    place = models.OneToOneField(Place, on_delete=models.CASCADE, related_name='stop', null=True)
    
    def __str__(self):
        return f"Stop: {self.name} (id: {self.pk})"
    
    class Meta:
        ordering = ['name']
    

class BusLine(models.Model):
    number = models.IntegerField(default='0')
    stops = models.ManyToManyField(BusStop, through="BusLineStop")
    
    def stops_list(self):
        """Returns the ordered list of the stops given by the line"""
        return [x.stop for x in BusLineStop.objects.filter(line=self).order_by('sequence')]
    
    def __str__(self):
        return f"Line: {self.number} - {self.first_stop} - {self.last_stop} (id: {self.pk})"
    
    @property
    def first_stop(self):
        return self.stops_list()[0].name if self.stops_list() else ''
    
    @property
    def last_stop(self):
        return self.stops_list()[-1].name if self.stops_list() else ''
    
    class Meta:
        ordering = ['number']


class BusLineStop(models.Model):
    stop = models.ForeignKey(BusStop, on_delete=models.CASCADE)
    line = models.ForeignKey(BusLine, on_delete=models.CASCADE)
    sequence = models.IntegerField(default='0') # stops of a given line are ordered by this sequence

    class Meta:
        ordering = ['sequence',]
        unique_together = (("line", "sequence"), )

    def __str__(self):
        return f"{self.line.number} - {self.stop.name} (id: {self.pk})"
