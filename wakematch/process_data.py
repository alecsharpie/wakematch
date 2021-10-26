import numpy as np
import pandas as pd
import pytz

from datetime import datetime, timedelta

def get_limits(user_timezone):

    user_now = datetime.now(tz=pytz.timezone(user_timezone))

    user_start = user_now - timedelta(hours=2)

    times = pd.date_range(user_start, periods=26, freq='1h').tolist()

    return [np.min(times), np.max(times)]


def inputs_to_rowdicts(user_timezone, input_name, input_timezone,
                       input_hourrange):

    start_hour, end_hour = input_hourrange[0], input_hourrange[1]

    user_now = datetime.now(tz=pytz.timezone(user_timezone))

    input_now = user_now.astimezone(pytz.timezone(input_timezone))

    input_start = input_now - timedelta(hours=2)

    times = pd.date_range(input_start, periods=26, freq='1h').tolist()

    #keep obs if they are the times of interest
    time_blips = [
        time for time in times
        if time.hour == start_hour or time.hour == end_hour
    ]

    # fill in missing start/end times
    if time_blips[0].hour == end_hour:
        time_blips.insert(0, np.min(times))
    if time_blips[-1].hour == start_hour:
        time_blips.insert(-1, np.max(times))

    # convert into users timezone
    user_timeblips = [
        time.astimezone(pytz.timezone(user_timezone)) for time in time_blips
    ]

    # create dictionary of rows for the inputs
    row_dict_list = []
    for x in range(int(len(user_timeblips) / 2)):
        row_dict_list.append({
            'person': input_name,
            'start': user_timeblips.pop(0),
            'end': user_timeblips.pop(0)
        })

    return row_dict_list


def input_to_dataframe(inputs):

    timezone_inputs = inputs[::2]

    hourrange_inputs = inputs[1::2]

    name_inputs = ['You'] + [
        f"Person {str(i + 1)}" for i in range(int(len(inputs) / 2 - 1))
    ]

    user_tz = timezone_inputs[0]

    all_waketimes = []
    for person in zip(name_inputs, timezone_inputs, hourrange_inputs):

        rowdict = inputs_to_rowdicts(user_timezone=user_tz,
                                     input_name=person[0],
                                     input_timezone=person[1],
                                     input_hourrange=person[2])

        all_waketimes = all_waketimes + rowdict

    return pd.DataFrame(all_waketimes)
