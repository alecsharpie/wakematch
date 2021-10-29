from datetime import datetime, timedelta
import pytz
import pandas as pd

def round_to_hour(time):
    return (time.replace(second=0, microsecond=0, minute=0, hour=time.hour) +
            timedelta(hours=time.minute // 30))


def get_times(user_timezone):

    user_now = datetime.now(tz=pytz.timezone(user_timezone))

    user_start = round_to_hour(user_now) - timedelta(hours=2)

    times = pd.date_range(user_start, periods=2 + 24 * 2, freq='1h').tolist()

    return times
