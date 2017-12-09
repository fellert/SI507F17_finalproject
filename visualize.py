import plotly
from plotly import tools
from plotly.graph_objs import *

def create_visual(stock_obj):
    ratings = ["BUY", "OUTPERFORM", "HOLD", "UNDERPERFORM", "SELL", "No Opinion"]
    rate_values = [stock_obj.ratings["BUY"] or None,
                   stock_obj.ratings["OUTPERFORM"] or None,
                   stock_obj.ratings["HOLD"] or None,
                   stock_obj.ratings["UNDERPERFORM"] or None,
                   stock_obj.ratings["SELL"] or None,
                   stock_obj.ratings["No Opinion"] or None]
    trace1 = Bar(
        x = ratings,
        y = rate_values,
        text = rate_values,
        textposition = 'auto',
        name = "Analyst Ratings",
        marker = dict(color='ffcb05'),
        hoverinfo = 'none'
    )
    targets = ["Current","High","Low","Median"]
    targ_values = [stock_obj.price,stock_obj.targets[1],stock_obj.targets[2],
                   stock_obj.targets[0]]
    trace2 = Bar(
        x = targets,
        y = targ_values,
        text = targ_values,
        textposition = 'auto',
        name = "Target Prices",
        marker = dict(color='00274c'),
        hoverinfo = 'none'
    )
    layout = Layout(
        title="Stock Ratings and Forecast for {}".format(stock_obj.name),
        font=dict(family='Open Sans, monospace', size=18, color='#7f7f7f'),
        xaxis1=dict(
            title='Ratings',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        ),
        yaxis1=dict(
            title='Number of Analysts',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        ),
        xaxis2=dict(
            title='Current and Predictions',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        ),
        yaxis2=dict(
            title='Price ($)',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        )
    )
    fig = tools.make_subplots(rows=2,cols=1,print_grid=False,subplot_titles=("Analyst Ratings", "Target Prices"))
    fig.append_trace(trace1, 1, 1)
    fig.append_trace(trace2, 2, 1)
    fig['layout'].update(layout)
    preference = input("\n##### VISUAL TO OPEN IN BROWSER AUTOMATICALLY? (TYPE YES OR NO): ").upper()
    if preference == "YES":
        plotly.offline.plot(fig,filename="wall_st_ratings.html")
    else:
        plotly.offline.plot(fig,filename="wall_st_ratings.html",auto_open=False)
