import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, MATCH, ALL

import plotly.express as px


import numpy as np
import pandas as pd
import pytz


ylabs = ['12am'] + [f"{str(x)}am" for x in range(1, 12)
                    ] + ['12pm'] + [f"{str(x)}pm" for x in range(1, 12)]

lab_dict = {k: v for k, v in zip(np.arange(0, 24), ylabs)}

app = dash.Dash(__name__,
                suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.Div([
        html.H1(children='WakeMatch', style={'textAlign': 'center'}),
        html.Div(children='Simple Timezone Matching',
                 style={'textAlign': 'center'})
    ]),
    dbc.Row([
        dbc.Col([
            html.Div(id='dropdown-container', children=[]),
            html.Div(id='dropdown-container-output'),
            html.Button("Add Filter", id="add-filter", n_clicks=0)
        ]),
        dbc.Col([
            html.Div("Hello World!"),
            html.Div("The Graph"),
            html.Div(id='timezone-comparison-graph-test'),
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
            'type': 'user-range',
            'index': n_clicks
        },
                     options=[{
                         'label': i,
                         'value': i
                     } for i in all_timezones]),
        dcc.RangeSlider(id={
            'type': 'user-range',
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


@app.callback(Output('timezone-comparison-graph-test', 'children'),
            Input({
                'type': 'user-range',
                'index': ALL
            }, 'value'))
def display_output(values):
    return html.Div([
        html.Div('Dropdown {} = {}'.format(i + 1, value))
        for (i, value) in enumerate(values)
    ])


@app.callback(dash.dependencies.Output('timezone-comparison-graph', 'figure'),
              Input({
                  'type': 'user-range',
                  'index': ALL
              }, 'value'))
def update_graph(values):

    df = pd.DataFrame([
        {'Task': values,
        'Start': 'user-range'
    }])

    [[8, 17],
     [8, 17]]




    df = pd.DataFrame([
        {'Task':"You", 'Start':'1996-02-12 08:00:00', 'Finish':'1996-02-12 17:00:00'},
        {'Task':"Person 1", 'Start':'1996-02-12 08:00:00', 'Finish' : '1996-02-12 17:00:00'}
    ])

    fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task")
    fig.update_yaxes(autorange="reversed") # otherwise tasks are listed from the bottom up


    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
