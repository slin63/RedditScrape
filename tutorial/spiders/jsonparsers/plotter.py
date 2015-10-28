import plotly.plotly as py
import plotly.graph_objs as go

py.sign_in('slin63', 'c3qo1fycv3')


def plot(stats_dic):
    data = [
        go.Bar(
            x=[key for key in stats_dic],
            y=[count[2] for count in stats_dic.values()]
        )
    ]

    py.plot(data, filename='reddit-bar')


