import plotly.express as px

from wakematch.process_data import get_limits

def create_graph(df, user_timezone):

    fig = px.timeline(df,
                      x_start="start",
                      x_end="end",
                      y="person",
                      range_x=get_limits(user_timezone),
                      color_discrete_sequence = ['#cc5500'])
    fig.update_yaxes(autorange="reversed") # otherwise tasks are listed from the bottom up

    return fig
