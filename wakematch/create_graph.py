import plotly.express as px

from wakematch.process_data import get_limits, find_waketimes


def create_graph(df, user_timezone):

    fig = px.timeline(df,
                      x_start="start",
                      x_end="end",
                      y="person",
                      range_x=get_limits(user_timezone),
                      color_discrete_sequence = ['#cc5500'])

    for idx, row in find_waketimes(df, user_timezone).iterrows():
        fig.add_vrect(x0=row['start'], x1=row['end'])

    # ({row['start'].astimezone(pytz.timezone('Europe/Zurich')).strftime('%I%p, %d %b, %Y')} and {row['end'].astimezone(pytz.timezone('Europe/Zurich')).strftime('%I%p, %d %b, %Y')} their time)

    fig.update_yaxes(
        tickfont={'size': 20},
        autorange="reversed")  # otherwise tasks are listed from the bottom up

    fig.update_layout(yaxis_title=None)
    return fig
