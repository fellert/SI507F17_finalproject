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
JSON, Requests, BeautifulSoup, Unittest, and Plotly.
