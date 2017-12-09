# 507 Final Project

This program is designed to take a stock ticker/symbol (e.g. AAPL for Apple)
and look up basic information about the stock. This is done by making BeautifulSoup
objects out of three URL requests to Bloomberg, CNN Money, and Reuters. The following
information is pulled from each site:

* Bloomberg - basin info (Price, name, trading volume)</li>
* CNN - price targets (high, median, low)</li>
* Reuters - Analyst ratings (i.e. Buy, Sell, Hold, etc.)</li>
