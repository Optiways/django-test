from django.db import models
from .fields import TsCreateField, TsUpdateField


class TsCreateUpdateMixin(models.Model):
    ts_create = TsCreateField()
    ts_update = TsUpdateField()

    class Meta:
        abstract = True
