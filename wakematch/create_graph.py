import plotly.express as px

def create_graph(df):

    fig = px.timeline(df, x_start="start", x_end="end", y="person")
    fig.update_yaxes(autorange="reversed") # otherwise tasks are listed from the bottom up


    return fig
