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

    time_diff = (pytz.timezone(input_tz).localize(date).astimezone(pytz.timezone(user_tz)) - pytz.timezone(user_tz).localize(date)).seconds//3600 * -1
    if time_diff != 0:
        return f"({time_diff} h)"
    return ""
