import plotly.plotly as py
import plotly.graph_objs as go

py.sign_in('slin63', 'c3qo1fycv3')

# stats_dic = {"thdwarffortress.jl": [25, 7, 10], "thAskReddit.jl": [27, 1, 3], "coleagueoflegends.jl": [3615, 780, 1077], "codwarffortress.jl": [421, 125, 167], "coAskReddit.jl": [4888, 1128, 1716], "thleagueoflegends.jl": [22, 7, 27]}


def separate_stats(stats_dic):
    comment_dic = {}
    thread_dic = {}

    for e in stats_dic:
        if e[0] == 'c':
            comment_dic[e] = stats_dic[e]
        elif e[0] == 't':
            thread_dic[e] = stats_dic[e]

    return comment_dic, thread_dic


def plot(stats_dic):
    new_dic = separate_stats(stats_dic)
    comment_dic = new_dic[0]
    thread_dic = new_dic[1]

    data_comments = go.Bar(
                x=[key for key in comment_dic],
                y=[(float(count[1])/count[0]) for count in comment_dic.values()],  # Percent of posts containing word searches
                name='Threads'
            )
    data_threads = go.Bar(
                x=[key for key in comment_dic],
                y=[(float(count[1])/count[0]) for count in thread_dic.values()],  # Percent of posts containing word searches
                name='Comments'
            )

    data = [data_comments, data_threads]
    layout = go.Layout(
        barmode='group',
        title='Percentage of posts containing keywords',
        xaxis=dict(
            title='Subreddit'
        ),
        yaxis=dict(
            title='Percentage'
        )
    )

    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='comment-bar')


    return 0


