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

Run pip install requirements.txt to install the required python packages, including
Requests, BeautifulSoup, psycopg2, urllib3, and Plotly. Other imported packages include
unittest and JSON. Plotly has both online (using and API) and offline modes - this program
uses the plotly.offline.plot to create graphs of stock data that will open in the
user's browser as localhost. In addition, all files are written to run using python3.6.

A PostgreSQL **database named FELLERT_SI507FINAL** will also need to be created in order for the
database.py file to connect and insert information.

To run the program after installing the required packages, simply type *python3 SI507F17_finalproject.py*
from the command line. You may also run the testing file as *python3 SI507F17_finalproject_tests.py*

# Running the Program

The program initially tries to open the "data.json" cache file, and when this fails (as it is not included)
it will create the file and run a loop creating url requests, a Stock() object, and inserting information
into the database/cache for five companies (AAPL, FB, XOM, AMZN, and GOOGL). This also fulfills the requirement
of having at least four rows in information in the database.

Once this is complete, the user will be show a prompt/instructions and asked to enter a stock ticker.
The program will check to see if the ticker is in the database or (if it is in the cache) if the timestamp
has expired. If either fail, a new request and object are created and information is entered/updated in the cache
and database. Otherwise the stock information is retrieved from the cache and a new object is created.

Some basic information is printed at the end of each run - company name, price and price targets, dividend yield,
approximate annual dividend payout, and consensus analyst rating (i.e buy, sell, hold, etc.). The user is then
prompted as to whether they would like a plotly graph to generate a html file and automatically open it in their
browser or if they would just like to save the file to the directory. After this, the user can either exit the
program or choose to enter another stock ticker.
