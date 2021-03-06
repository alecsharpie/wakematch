import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL

import pytz

from wakematch.process_dates import calc_time_diff
from wakematch.process_data import input_to_dataframe, find_waketimes, check_or
from wakematch.create_graph import create_graph


app = dash.Dash(__name__,
                suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ])

server = app.server

app.index_string = """<!DOCTYPE html>
<html>
    <head>
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-31EJTGBS39"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());

            gtag('config', 'G-31EJTGBS39', { 'anonymize_ip': true });
        </script>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>"""

app.title = 'WakeTimes'

app.layout = html.Div([
    html.Div([
        html.H1(children='WakeTimes', style={'textAlign': 'center'}),
        html.Div(children='Simple Timezone Matching',
                 style={'textAlign': 'center'})
    ]),
    dbc.Row(
        dbc.Col([
            html.Div(id='dropdown-container',
                     children=[],
                     style={
                         'display': 'flex',
                         'flex-flow': 'row wrap'
                     }),
            dbc.Button(" + Add Person",
                       id="add-person",
                       n_clicks=0,
                       style={
                           'margin': '10px',
                           'padding': '3px'
                       }),
            html.Hr(style={
                'margin': '0px',
                'padding': '0px'
            })
        ])),
    dbc.Row([
        dbc.Col([html.Div(id='timezone-comparison')],
                xs = 12, sm = 12, md = 12, lg = 4, xl = 4, xxl = 4),
        dbc.Col([dcc.Graph(id='timezone-comparison-graph'),
                 html.Div([html.Span('Yellow', style = {'color': '#FCB01C'}),
                           html.Span(' means an individual is awake, '),
                           html.Span('Blue',style = {'color': '#008CEF'}),
                           html.Span(' shows a Match!')],
                          style = {'margin': '0px 0px 0px 0px'})],
                xs = 12, sm = 12, md = 12, lg = 8, xl = 8, xxl = 8)
    ],
            style={'padding': '20px'}),
    dbc.Row([
        dbc.Col([html.Hr(style={
                'margin': '0px',
                'padding': '0px'
            }),
            html.Div(['Made by ', dcc.Link('Alec Sharp', href ='https://www.alecsharpie.me')])], style={'padding': '30px'})])
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
                     value='Australia/Victoria',
                     style = {'margin': '5px'}),
        dcc.RangeSlider(id={
            'type': 'user-inputs',
            'index': n_clicks
        },
                        min=0,
                        max=23,
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
                        value=[8, 22])
    ],
                            style={
                                'width': '100%',
                                'max-width' : '400px',
                                'padding': '0px 10px 10px 10px'
                            })
    children.append(new_dropdown)
    return children

@app.callback(Output('timezone-comparison', 'children'),
              Input({
                  'type': 'user-inputs',
                  'index': ALL
              }, 'value'))
def update_comparison(values):

    if len(values) > 0:

        df = input_to_dataframe(values)

        waketimes = find_waketimes(df, user_timezone = values[0])

        comparison_text = html.Div([
            html.Div(f'Available Times:', style={'font-size': '28px',
                                                 'padding-bottom': '15px'})
        ] + [
            html.Div([
                html.Div([
                    html.Span(
                        f"{row['start'].astimezone(pytz.timezone(tz)).strftime('%a, %-I %p')}",
                        style={'font-weight': 'bold'}), " to ",
                    html.Span(
                        f"{row['end'].astimezone(pytz.timezone(tz)).strftime('%a, %-I %p')}",
                        style={'font-weight': 'bold'}),
                    html.Span(f" {tz} {calc_time_diff(row['start'].replace(tzinfo=None), user_tz = values[0], input_tz = tz)}"),
                    html.Br()
                ]) for tz in df.tz.unique()
            ] + [
                html.Div(check_or(idx, waketimes), style = {'line-height': '3'})
            ]) for idx, row in waketimes.iterrows()
        ])

        return comparison_text

    return html.Div([])


@app.callback(Output('timezone-comparison-graph', 'figure'),
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
