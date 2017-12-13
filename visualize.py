import plotly
from plotly import tools
from plotly.graph_objs import *
from database import *

# MAKES TWO QUERIES TO THE DATABASE FOR TARGET PRICES AND ANALYST RATINGS
# IN ORDER TO BUILD TWO PLOTLY BAR CHARTS
def create_visual(stock_name, stock_price, testing=False):
    ratings = ["BUY", "OUTPERFORM", "HOLD", "UNDERPERFORM", "SELL", "No Opinion"]
    cur.execute("SELECT * FROM Ratings WHERE Ratings.stock_id = \
                (SELECT Company.id from Company WHERE Company.name = %s)", (stock_name,))
    rate_query = cur.fetchall()
    rate_query = rate_query[0]
    rate_values = [rate_query[2], rate_query[3], rate_query[4], rate_query[5],
                   rate_query[6], rate_query[7]]
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
    targets = ["Current","Median","High","Low"]
    cur.execute("SELECT * FROM Targets WHERE Targets.stock_id = \
                (SELECT Company.id from Company WHERE Company.name = %s)", (stock_name,))
    targ_query = cur.fetchall()
    targ_query = targ_query[0]
    targ_values = [stock_price, targ_query[2], targ_query[3], targ_query[4]]
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
        title="Stock Ratings and Forecast for {}".format(stock_name),
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
    # THE TEST FILE CREATES AN OBJECT FOR THE WALT DISNEY COMPANY, AND TESTS THE CREATE_VISUAL FUNCTION
    # TO MAKE SURE IT ACTUALLY CREATES AN HTML PAGE - THIS IS WHY THE NAME IS DIFFERENT - TO BE SPECIFIC TO
    # THAT TEST FUNCTION
    if testing == False:
        plotly.offline.plot(fig,filename="stock_info.html")
    else:
        plotly.offline.plot(fig,filename="DIS_info.html", auto_open=False)
