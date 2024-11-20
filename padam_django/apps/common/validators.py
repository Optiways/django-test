import datetime

from django.core.exceptions import ValidationError


def validate_future_date(value: datetime.datetime):
    now = datetime.datetime.now(tz=datetime.timezone.utc)
    if value < now:
        raise ValidationError(
            "%(value)s is set before the current date %(now)s",
            params={"value": value.isoformat(), "now": now.isoformat()},
        )
