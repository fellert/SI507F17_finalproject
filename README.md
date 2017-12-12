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

After pulling information from the BeautifulSoup objects and storing it into a dictionary,
the program then uses this info to create/instantiate a Stock() object - including a constructor with basic information,
a repr method, a method that finds an approximate annual dividend payout using the dividend yield, a
contains method that converts the mean analyst rating into a sentiment (Bullish or Bearish) and
checks if this matched the user input, a consensus method which finds the rating with most analyst support
(i.e. Buy, Sell, Hold, etc.), and a price_targets method that prints out the 12-month targets in a bullet format.


## Overview of Files

* **SI507F17_finalproject.py**
  * Contains the code that runs the program loop to make the url requests, construct the Stock() object,
    and build a dictionary entry to be added to the cache (if needed) for a user-entered ticker.
* **SI507F17_finalproject_tests.py**
  * Contains four classes and 16 methods that test the functions, caching, databases, and edge cases
    (i.e. if a ticker does not exist or if some information like the analyst ratings are unavailable).
* **visualize.py**
  * Contains code to construct two plotly bar graph, as well as the additional formatting dictionary
    (to change colors, add labels/titles, etc.).
* **database.py**
  * Contains three functions - one that builds the database tables the first time the program is run,
    one that inserts a stock's information the first time it is sentiment, one that updated a stock's
    information if the cache timestamp has expired.
* **config.py**
  * Contains the required dbname and an empty user field (for whoever runs the program).
* **screenshots**
  * Contains screenshots of every table in the database with the automatically inserted 5 companies, a plotly chart for Amazon,
    two of the command line - when the program is first run, and then for requests to AAPL (in cache), MSFT (not in cache, makes new request), GELYF (does not have any price targets), and DL (does not have any analyst ratings, so consensus cannot be made)

## Installation/Requirements

* Run *pip install -r requirements.txt* to install the required python packages, including
   Requests, BeautifulSoup, psycopg2, and Plotly.
* Plotly has both online (using and API) and offline modes - this program
   uses the plotly.offline.plot to create graphs of stock data that will open directly in the
   user's browser - there is no need for API keys or secret data.
* All files are written to run using python 3.6.
* A PostgreSQL database called **FELLERT_SI507FINAL** needs to be created. The config file
   contains an empty user="" field, which may also be filled out.
* You can start your postgres database by typing pg_ctl -D /usr/local/var/postgres start

To run the program after installing the required packages, simply type *python3 SI507F17_finalproject.py*
from the command line. You may also run the testing file as *python3 SI507F17_finalproject_tests.py*.

## Running the Program

### Full Process:
1 Clone/download the repository, create database FELLERT_SI507FINAL (and enter user="" info),
  and install the proper packages by typing pip install -r requirements.txt.
1 Run the program by typing *python3 SI507F17_finalproject* from the command line. As the cache is not included in the
  repository, the first time the program runs it will create a file called "data.json", make requests, BeautifulSoup
  and Stock() objects, and insert stock information for 5 companies (AAPL, FB, XOM, AMZN, and GOOGL) into the cache and database.
3 The user will then be prompted to enter a stock ticker, in which the program then:
  * Looks to see if the ticker is in the cache - if not, it makes requests, BeautifulSoup and Stock() objects.
  * If in the cache, it checks the timestamp and will run again if expired.
  * If both pass, it will pull information from the cache and make a Stock() object.
  * If the first two cases, the program will then update the cache and either create a new entry or update the database.
4 Some basic information about the stock is then printed.
5 The program will then generate a plotly HTML file "stock_info.html", but the user has a choice as to automatically open
  a browser tab to display the chart or to skip. Each chart displays the 12-month price targets and analyst ratings. An example of the expected final result, labeled "amazon_plotly" may be found in the repository in the screenshots directory.
6 The user is then prompted to enter another ticker or exit.

### Tests File and Important Note:
SI507F17_finalproject_tests.py can be run by simply typing *pyhton SI507F17_finalproject_tests.py* from the command line.
Four classes and 16 methods will then be executed (all of which should pass). One important note is that one method tests the contains function, which checks if a sentiment input (Bullish for stocks that are a buy, and Bearish for those that are a sell) is in the stock's analyst ratings. It does this by converting the mean rating (on a scale of 1-5, lower numbers are a buy, while
higher ones are sell). Because markets change by the day, there is a small change the analysts ratings could change and alter the mean rating, possibly throwing off the test. Just to be sure, I chose a stock that has been a buy for a long time, so this is unlikely.

## Additional Links

### Example Pages Used for BeautifulSoup
* Example CNN Money request: http://money.cnn.com/quote/quote.html?symb=AAPL
* Example Bloomberg request: https://www.bloomberg.com/quote/AAPL:US
* Example Reuters request: https://www.reuters.com/finance/stocks/overview/AAPL.OQ

### Links to Package Documentation
* Plotly installation: https://plot.ly/python/getting-started/
* Plotly guide on bar charts: https://plot.ly/python/bar-charts/
* Plotly guide for subplots (graphing to charts on one page): https://plot.ly/python/subplots/
* BeautifulSoup documentation: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
* Requests documentation: http://docs.python-requests.org/en/master/
* psycopg2 documentation: http://initd.org/psycopg/docs/
