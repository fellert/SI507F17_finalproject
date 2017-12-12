import plotly
from plotly import tools
from plotly.graph_objs import *

# TAKES THE STOCK OBJECT AND TICKER (FOR THE OUTPUT FILE NAME) TO CREATE A
# PLOTLY BAR CHART
def create_visual(stock_obj, ticker, testing=False):
    ratings = ["BUY", "OUTPERFORM", "HOLD", "UNDERPERFORM", "SELL", "No Opinion"]
    rate_values = [stock_obj.ratings["BUY"],
                   stock_obj.ratings["OUTPERFORM"],
                   stock_obj.ratings["HOLD"],
                   stock_obj.ratings["UNDERPERFORM"],
                   stock_obj.ratings["SELL"],
                   stock_obj.ratings["No Opinion"]]
    # CREATES BAR CHART FOR ANALYST RATINGS
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
    # USES TARGETS ABOVE TO CREATE BAR CHART FOR PRICE FORECASTS
    trace2 = Bar(
        x = targets,
        y = targ_values,
        text = targ_values,
        textposition = 'auto',
        name = "Target Prices",
        marker = dict(color='00274c'),
        hoverinfo = 'none'
    )
    # SOME FORMATTING (AXES NAMES, BAR COLORS, ETC.)
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
    # DO NOT CREATE PLOTS WHEN RUNNING THE TEST PROGRAM (WHICH WILL CREATE SEVERAL STOCK OBJECTS)
    if testing == False:
        plotly.offline.plot(fig,filename="stock_info.html")
    else:
        plotly.offline.plot(fig,filename="stock_info.html", auto_open=False)
