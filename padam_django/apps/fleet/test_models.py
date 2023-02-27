from django.forms import ValidationError
import pytest

from .factories import BusShiftFactory, BusStopFactory


@pytest.mark.django_db
def test_shift_throw_no_stop():
    shift = BusShiftFactory()
    with pytest.raises(ValidationError):
        shift.clean()


@pytest.mark.django_db
def test_shift_do_not_throw_with_2stops():
    shift = BusShiftFactory()
    BusStopFactory(shift=shift)
    BusStopFactory(shift=shift)
    shift.clean()


@pytest.mark.django_db
def test_shift_rasie_with_1stop():
    shift = BusShiftFactory()
    BusStopFactory(shift=shift)
    with pytest.raises(ValidationError):
        shift.clean()
