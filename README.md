# 507 Final Project

## Description

This program is designed to take a stock ticker/symbol (e.g. AAPL for Apple)
and look up basic information about the stock. This is done by making BeautifulSoup
objects out of three URL requests to Bloomberg, CNN Money, and Reuters, and scraping
each site for the following data:

Website    | Data
---------- | -------------
Bloomberg  | basic information (company name, price, trading volume, dividend yield)
CNN Money  | 12-month price targets (median, high, low)
Reuters    | Analyst ratings (buy, outperform, hold, underperform, sell, no opinion)

## Overview of Files

* SI507F17_finalproject.py
  * Contains the code that runs the program loop to make the url requests, construct the Stock() object,
    and build a dictionary entry to be added to the cache (if needed) for a user-entered ticker
* SI507F17_finalproject_tests.py
  * Contains three classes and 16 methods that test the functions, caching, databases, and edge cases
* visualize.py
  * Contains code to construct two plotly bar graph, as well as the additional formatting dictionary
    (to change colors, add labels/titles, etc.)
* database.py
  * Contains three functions
    * one that builds the database tables the first time the program is run,
    * one that inserts a stock's information the first time it is sentiment
    * one that updated a stock's information if the cache timestamp has expired 

## Installation/Requirements

Run pip install requirements.txt to install the required python packages, including
Requests, BeautifulSoup, psycopg2, urllib3, and Plotly. Other imported packages include
unittest and JSON. Plotly has both online (using and API) and offline modes - this program
uses the plotly.offline.plot to create graphs of stock data that will open in the
user's browser as localhost. In addition, all files are written to run using python3.6

To run the program after installing the required packages, simply type *python3 SI507F17_finalproject.py*
from the command line. You may also run the testing file as *python3 SI507F17_finalproject_tests.py*
