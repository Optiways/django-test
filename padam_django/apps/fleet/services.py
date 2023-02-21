from typing import Tuple
from datetime import datetime, date, time
from dateutil.relativedelta import relativedelta


def get_time_diff_between(time_field: time, time_field2: time) -> Tuple[int, int]:
    date_time = datetime.combine(date.today(), time_field)
    date_time2 = date_time.combine(date.today(), time_field2)
    diff_time = relativedelta(date_time2, date_time)
    return diff_time.hours, diff_time.minutes
