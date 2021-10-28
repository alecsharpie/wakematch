import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL

import pytz

from wakematch.process_data import input_to_dataframe
from wakematch.create_graph import create_graph


app = dash.Dash(__name__,
                suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.Div([
        html.H1(children='WakeTimes', style={'textAlign': 'center'}),
        html.Div(children='Simple Timezone Matching',
                 style={'textAlign': 'center'})
    ]),
    dbc.Row([
        dbc.Col([
            html.Div(id='dropdown-container', children=[]),
            html.Div(id='dropdown-container-output'),
            html.Button("Add Person", id="add-person", n_clicks=0)
        ], width = 4),
        dbc.Col([dcc.Graph(id='timezone-comparison-graph')], width = 8)
    ],
            style={'padding': '20px'})
])


@app.callback(Output('dropdown-container', 'children'),
              Input('add-person', 'n_clicks'),
              State('dropdown-container', 'children'))
def display_dropdowns(n_clicks, children):

    all_timezones = list(pytz.all_timezones_set)


    display_name =  f'Person {n_clicks}'

    if n_clicks == 0:
        display_name = 'You'


    new_dropdown = html.Div([
        html.Div(display_name),
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
                            1: '',
                            2: '',
                            3: '3am',
                            4: '',
                            5: '',
                            6: '6am',
                            7: '',
                            8: '',
                            9: '9am',
                            10: '',
                            11: '',
                            12: '12pm',
                            13: '',
                            14: '',
                            15: '3pm',
                            16: '',
                            17: '',
                            18: '6pm',
                            19: '',
                            20: '',
                            21: '9pm',
                            22: '',
                            23: ''
                        },
                        value=[8, 17])
    ],
                            style={'display': 'block',
                                'padding-bottom': '10px'})
    children.append(new_dropdown)
    return children


@app.callback(dash.dependencies.Output('timezone-comparison-graph', 'figure'),
              Input({
                  'type': 'user-inputs',
                  'index': ALL
              }, 'value'))
def update_graph(values):

    if len(values) > 0 :

        df = input_to_dataframe(values)

        fig = create_graph(df, user_timezone = values[0])

        return fig
    return {}

if __name__ == '__main__':
    app.run_server(debug=True)
