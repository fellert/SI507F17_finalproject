# 507 Final Project

## Description

This program is designed to take a stock ticker/symbol (e.g. AAPL for Apple)
and look up basic information about the stock. This is done by making BeautifulSoup
objects out of three URL requests to Bloomberg, CNN Money, and Reuters, and scraping
each site for the following data:

* Bloomberg - basin info (Price, name, trading volume)
* CNN - price targets (high, median, low)</li>
* Reuters - Analyst ratings (i.e. Buy, Sell, Hold, etc.)



## Installation/Requirements

Run pip install requirements.txt to install the required python packages, including
Requests, BeautifulSoup, psycopg2, urllib3, and Plotly. Other imported packages include
unittest and JSON. Plotly has both online (using and API) and offline modes - this program
uses the plotly.offline.plot to create graphs of stock data that will open in the
user's browser as localhost. In addition, all files are written to run using python3.6 

To run the program after installing the required packages, simply type *python3 SI507F17_finalproject.py*
from the command line. You may also run the testing file as *python3 SI507F17_finalproject_tests.py*
