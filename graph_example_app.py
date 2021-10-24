# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

from datetime import date


app = dash.Dash(__name__)

colors = {'background': '#fff', 'text': '#7FDBFF'}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

fig.update_layout(plot_bgcolor=colors['background'],
                  paper_bgcolor=colors['background'],
                  font_color=colors['text'])

app.layout = html.Div(style={'backgroundColor': colors['background']},
                      children=[
                          html.H1(children='WakeMatch',
                                  style={
                                      'textAlign': 'center',
                                      'color': colors['text']
                                  }),
                          html.Div(children='Simple Timezone Matching',
                                   style={
                                       'textAlign': 'center',
                                       'color': colors['text']
                                   }),
                          dcc.RangeSlider(id='my-range-slider',
                                          min=0,
                                          max=20,
                                          step=0.5,
                                          value=[5, 15]),
                          html.Div(id='output-container-range-slider'),
                          dcc.Graph(id='example-graph-2', figure=fig)
                      ])


@app.callback(
    dash.dependencies.Output('output-container-range-slider', 'children'),
    [dash.dependencies.Input('my-range-slider', 'value')])
def update_output(value):
    return 'You have selected "{}"'.format(value)


if __name__ == '__main__':
    app.run_server(debug=True)
