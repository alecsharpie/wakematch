import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, MATCH, ALL

import plotly.express as px


import numpy as np
import pandas as pd
import pytz

from datetime import datetime, timedelta


def inputs_to_rowdicts(user_timezone, input_name, input_timezone,
                       input_hourrange):

    start_hour, end_hour = input_hourrange[0], input_hourrange[1]

    user_now = datetime.now(tz=pytz.timezone(user_timezone))

    input_now = user_now.astimezone(pytz.timezone(input_timezone))

    input_start = input_now - timedelta(hours=24)

    times = pd.date_range(input_start, periods=72, freq='1h').tolist()

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


# ylabs = ['12am'] + [f"{str(x)}am" for x in range(1, 12)
#                     ] + ['12pm'] + [f"{str(x)}pm" for x in range(1, 12)]

# lab_dict = {k: v for k, v in zip(np.arange(0, 24), ylabs)}

app = dash.Dash(__name__,
                suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.Div([
        html.H1(children='WakeMatch', style={'textAlign': 'center'}),
        html.Div(children='Simple Timezone Matching',
                 style={'textAlign': 'center'}),
        html.Div(
    [
        html.H1(id="date-time-title"),
        dcc.Interval(id="clock", interval=1000)
    ])

    ]),
    dbc.Row([
        dbc.Col([
            html.Div(id='dropdown-container', children=[]),
            html.Div(id='dropdown-container-output'),
            html.Button("Add Filter", id="add-filter", n_clicks=0)
        ]),
        dbc.Col([
            dcc.Graph(id='timezone-comparison-graph')
        ])
    ])
])


@app.callback(Output('dropdown-container', 'children'),
              Input('add-filter', 'n_clicks'),
              State('dropdown-container', 'children'))
def display_dropdowns(n_clicks, children):

    all_timezones = list(pytz.all_timezones_set)

    new_dropdown = html.Div([
        html.Div(f"Person"),
        dcc.Dropdown(id={
            'type': 'user-inputs',
            'index': n_clicks
        },
                     options=[{
                         'label': i,
                         'value': i
                     } for i in all_timezones],
                     value='Australia/Victoria'),
        dcc.RangeSlider(id={
            'type': 'user-inputs',
            'index': n_clicks
        },
                        min=0,
                        max=24,
                        step=None,
                        marks={
                            0: '12am',
                            1: '1am',
                            2: '2am',
                            3: '3am',
                            4: '4am',
                            5: '5am',
                            6: '6am',
                            7: '7am',
                            8: '8am',
                            9: '9am',
                            10: '10am',
                            11: '11am',
                            12: '12pm',
                            13: '1pm',
                            14: '2pm',
                            15: '3pm',
                            16: '4pm',
                            17: '5pm',
                            18: '6pm',
                            19: '7pm',
                            20: '8pm',
                            21: '9pm',
                            22: '10pm',
                            23: '11pm'
                        },
                        value=[8, 17])
    ],
                            style={'display': 'block'})
    children.append(new_dropdown)
    return children


@app.callback(dash.dependencies.Output('timezone-comparison-graph', 'figure'),
              Input({
                  'type': 'user-inputs',
                  'index': ALL
              }, 'value'))
def update_graph(values):

    df = input_to_dataframe(values)

    fig = px.timeline(df, x_start="start", x_end="end", y="person")
    fig.update_yaxes(autorange="reversed") # otherwise tasks are listed from the bottom up

    return fig

def input_to_dataframe(inputs):

    timezone_inputs = inputs[::2]

    hourrange_inputs = inputs[1::2]

    name_inputs = ['You'] + [f"Person {str(i + 1)}" for i in range(int(len(inputs)/2 - 1))]

    user_tz = timezone_inputs[0]

    all_waketimes = []
    for person in zip(name_inputs, timezone_inputs, hourrange_inputs):

        rowdict = inputs_to_rowdicts(user_timezone = user_tz,
                                    input_name = person[0],
                                    input_timezone = person[1],
                                    input_hourrange = person[2])

        all_waketimes = all_waketimes + rowdict

    return pd.DataFrame(all_waketimes)


if __name__ == '__main__':
    app.run_server(debug=True)
