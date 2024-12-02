from datetime import datetime

import pytest

from padam_django.apps.geography.utils import is_shifts_compatible

shifts_test_cases = [
    (datetime(2001, 12, 10), datetime(2001, 12, 13), datetime(2001, 12, 9), datetime(2001, 12, 11), False),
    (datetime(2001, 12, 10), datetime(2001, 12, 13), datetime(2001, 12, 11), datetime(2001, 12, 12), False),
    (datetime(2001, 12, 10), datetime(2001, 12, 13), datetime(2001, 12, 11), datetime(2001, 12, 14), False),
    (datetime(2001, 12, 10), datetime(2001, 12, 13), datetime(2001, 12, 9), datetime(2001, 12, 14), False),
    (datetime(2001, 12, 10), datetime(2001, 12, 13), datetime(2001, 12, 8), datetime(2001, 12, 9), True),
    (datetime(2001, 12, 10), datetime(2001, 12, 13), datetime(2001, 12, 14), datetime(2001, 12, 15), True),
]


@pytest.mark.parametrize("departure_a, arrival_a, departure_b, arrival_b, expected", shifts_test_cases)
def test_check_shifts_compatibility(departure_a, arrival_a, departure_b, arrival_b, expected):
    computed_compatibility = is_shifts_compatible(departure_a, arrival_a, departure_b, arrival_b)
    assert computed_compatibility == expected
