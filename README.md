# 507 Final Project

## Description

This program is designed to take a stock ticker/symbol (e.g. AAPL for Apple)
and look up basic information about the stock. This is done by making BeautifulSoup
objects out of three URL requests to Bloomberg, CNN Money, and Reuters, and scraping
each site for the following data:

Website    | Data
---------- | -------------
Bloomberg  | Basic information (company name, price, trading volume, dividend yield)
CNN Money  | 12-month price targets (median, high, low)
Reuters    | Analyst ratings (buy, outperform, hold, underperform, sell, no opinion)


## Overview of Files

* **SI507F17_finalproject.py**
  * Contains the code that runs the program loop to make the url requests, construct the Stock() object,
    and build a dictionary entry to be added to the cache (if needed) for a user-entered ticker
* **SI507F17_finalproject_tests.py**
  * Contains three classes and 16 methods that test the functions, caching, databases, and edge cases
    (i.e. if a ticker does not exist or if some information like the analyst ratings are unavailable)
* **visualize.py**
  * Contains code to construct two plotly bar graph, as well as the additional formatting dictionary
    (to change colors, add labels/titles, etc.)
* **database.py**
  * Contains three functions - one that builds the database tables the first time the program is run,
    one that inserts a stock's information the first time it is sentiment, one that updated a stock's
    information if the cache timestamp has expired


## Installation/Requirements

 * Run *pip install -r requirements.txt* to install the required python packages, including
   Requests, BeautifulSoup, psycopg2, and Plotly.
 * Plotly has both online (using and API) and offline modes - this program
   uses the plotly.offline.plot to create graphs of stock data that will open directly in the
   user's browser - there is no need for API keys or secret data.
 * All files are written to run using python 3.6.
 * A PostgreSQL database called **FELLERT_SI507FINAL** needs to be created. The connection
   function is at the top of the database.py file and has an empty user="" field that can
   also be filled in.


To run the program after installing the required packages, simply type *python3 SI507F17_finalproject.py*
from the command line. You may also run the testing file as *python3 SI507F17_finalproject_tests.py*

## Running the Program

### Process:
* Clone/download the repository, create database FELLERT_SI507FINAL, and install the proper packages using
  pip install -r requirements.txt
* Run the program by typing *python3 SI507F17_finalproject*. As the cache is not included in the repository,
  the first time the program is run it will create a file called "data.json", make requests, BeautifulSoup
  objects and input stock information for 5 companies (AAPL, FB, XOM, AMZN, and GOOGL)
* The user will then be prompted to enter a stock ticker, in which the program then:
  * Looks to see if the ticker is in the cache - if not it makes requests, BeautifulSoup, and Stock() object
  * If in the cache, it checks the timestamp and will run again if expired
  * If both pass, it will pull information from the cache and make a Stock() object
  * If the first two cases, the program will then update the cache and either enter/update the database
* Some basic information about the stock is then printed
* The program will then generate a plotly HTML file, but the user has a choice as to automatically open
  a browser tab or skip
* The user is then prompted to enter another ticker or exit


## Additional Links

* Example CNN Money request: http://money.cnn.com/quote/quote.html?symb=AAPL
* Example Bloomberg request: https://www.bloomberg.com/quote/AAPL:US
* Example Reuters request: https://www.reuters.com/finance/stocks/overview/AAPL.OQ

* Plotly guide on bar charts: https://plot.ly/python/bar-charts/
* Plotly guide for subplots (graphing to charts on one page): https://plot.ly/python/subplots/
