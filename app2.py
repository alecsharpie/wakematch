import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH, ALL

import numpy as np

ylabs = ['12am'] + [f"{str(x)}am" for x in range(1, 12)
                    ] + ['12pm'] + [f"{str(x)}pm" for x in range(1, 12)]

lab_dict = {k: v for k, v in zip(np.arange(0, 24), ylabs)}

app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([
    html.Button("Add Filter", id="add-filter", n_clicks=0),
    html.Div(id='dropdown-container', children=[]),
    html.Div(id='dropdown-container-output'),
    dcc.RangeSlider(min=0,
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
])


@app.callback(Output('dropdown-container', 'children'),
              Input('add-filter', 'n_clicks'),
              State('dropdown-container', 'children'))
def display_dropdowns(n_clicks, children):
    new_dropdown = html.Div([
        dcc.Dropdown(id={
            'type': 'filter-dropdown',
            'index': n_clicks
        },
                     options=[{
                         'label': i,
                         'value': i
                     } for i in ['NYC', 'MTL', 'LA', 'TOKYO']]),
        html.Div("Hello World!"),
        dcc.RangeSlider(
            min=0, max=24, step=None, marks=lab_dict, value=[8, 17])
    ],
                            style={'display': 'inline-block'})
    children.append(new_dropdown)
    return children


@app.callback(Output('dropdown-container-output', 'children'),
              Input({
                  'type': 'filter-dropdown',
                  'index': ALL
              }, 'value'))
def display_output(values):
    return html.Div([
        html.Div('Dropdown {} = {}'.format(i + 1, value))
        for (i, value) in enumerate(values)
    ])


if __name__ == '__main__':
    app.run_server(debug=True)
