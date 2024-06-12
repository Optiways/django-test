import factory
from faker import Faker

from . import models


fake = Faker(['fr'])


class BusShiftFactory(factory.django.DjangoModelFactory):
    name = factory.LazyFunction(fake.user_name)

    class Meta:
        model = models.BusShift
