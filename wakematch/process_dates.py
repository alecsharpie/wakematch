from datetime import datetime, timedelta
import pytz
import pandas as pd
import numpy as np

def round_to_hour(time):
    return (time.replace(second=0, microsecond=0, minute=0, hour=time.hour) +
            timedelta(hours=time.minute // 30))


def get_times(user_timezone):

    user_now = datetime.now(tz=pytz.timezone(user_timezone))

    user_start = round_to_hour(user_now) - timedelta(hours=2)

    times = pd.date_range(user_start, periods=2 + 24 * 2, freq='1h').tolist()

    return times

def calc_time_diff(date, user_tz, input_tz):

    if user_tz == input_tz:
        return ""

    user_utcoffset = pytz.timezone(user_tz).localize(date).utcoffset()
    input_utcoffset = pytz.timezone(input_tz).localize(date).utcoffset()

    time_diff = input_utcoffset - user_utcoffset

    hours = time_diff.total_seconds()/3600

    hours_str = f"{hours} h"

    if hours > 0:
        hours_str = f'+{hours_str}'
    return hours_str
