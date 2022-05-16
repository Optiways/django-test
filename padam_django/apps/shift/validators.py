from django.core.exceptions import ValidationError
from django.utils import timezone

"""
verify that bus stop is not set in the past
"""
def validate_stop_datetime(datetime):
    if datetime < timezone.now():
        raise ValidationError("Date cannot be in the past")

