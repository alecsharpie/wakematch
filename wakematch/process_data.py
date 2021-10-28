import numpy as np
import pandas as pd
import pytz

from datetime import datetime, timedelta

from wakematch.process_dates import get_times

def get_limits(user_timezone):

    times = get_times(user_timezone)

    return [np.min(times), np.max(times)]


def inputs_to_rowdicts(user_timezone, input_name, input_timezone,
                       input_hourrange):

    start_hour, end_hour = input_hourrange[0], input_hourrange[1]

    times = get_times(input_timezone)

    #keep obs if they are the times of interest
    time_blips = [
        time for time in times
        if time.hour == start_hour or time.hour == end_hour
    ]

    # fill in missing start/end times
    if time_blips[0].hour == end_hour:
        time_blips.insert(0, np.min(times))
    if time_blips[-1].hour == start_hour:
        time_blips.append(np.max(times))

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
        # start and end are swapped
        # print(rowdict)
        all_waketimes = all_waketimes + rowdict

    return pd.DataFrame(all_waketimes)


def find_match(df, user_timezone):

    # contains all 3 intervals
    #print(df)

    times = get_times(user_timezone)
    #print(times)
    time_dict = {}
    for time in times:
        n_wakes = 0
        for idx, row in df.iterrows():
            if time >= row['start'] and time <= row['end']:
                n_wakes += 1
        time_dict[time] = n_wakes

    # only the first interval is being counted
    # when count should be 3 its 2 or 1
    #print(time_dict)

    matches = {
        k: v
        for k, v in time_dict.items() if v == len(df.person.unique())
    }.keys()

    # does not contain all matches
    #print(matches)

    return matches


def find_waketimes(df, user_timezone):
    x = [match for match in find_match(df, user_timezone)]
    # find match is not working
    #print(x)

    # # this loop does not find all occurances
    # # you shuold find all occurances first
    # # and use this to break up the list?
    # timeslots_list = []
    # diff_list = []
    # for i in range(len(x) - 1):
    #     if ((x[i + 1] - x[i]) > np.timedelta64(1,
    #                                            'h')):  # or (i+1 == len(x)-1):
    #         diff_list.append(i)

    # if len(diff_list) == 0:
    #     intervals = [x]

    # if len(diff_list) == 1:
    #     intervals = x[:diff_list[0]+1] + x[diff_list[0]+1:]

    # if len(diff_list) > 1:
    #     waketimes_list = []
    #     intervals = x[:diff_list[0]+1] + x[diff_list[-1]+1:] + waketimes_list

    #     for diff in diff_list:
    #         pass




    # intervals = timeslots_list + [x]

    timeslots_list = []
    for i in range(len(x) - 1):
        if ((x[i + 1] - x[i]) > np.timedelta64(1,
                                               'h')):  # or (i+1 == len(x)-1):
            timeslots_list.append(x[:i + 1])
            x = x[i + 1:]

    intervals = timeslots_list + [x]

    #second bars not counting in match-ups
    #print(intervals)

    intervals = [interval for interval in intervals if len(interval) > 1]

    return pd.DataFrame([{
        'start': np.min(interval),
        'end': np.max(interval)
    } for interval in intervals])
