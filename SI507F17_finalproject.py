import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from database import *
from visualize import *

# FOR USE IN CHECKING IF CACHE ENTRY HAS EXPIRED
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

# CLASS THAT CREATES A STOCK OBJECT FOR A PARTICULAR STOCK, GIVEN 3 SOUP OBJECTS
class Stock(object):
    def __init__(self,dictionary):
        self.dict = dictionary
        self.name = self.dict['name']
        self.price = self.dict['price']
        self.targets = self.dict['targets']
        self.volume = self.dict['volume']
        self.ratings = self.dict['ratings']
        self.mean = self.dict['mean rating']
        self.dividend = self.dict['dividend']

    def __repr__(self):
        return "The most recent price for {} is ${}".format(self.name,self.price)

    # CONVERTS MEAN RATING (SELF.MEAN) INTO A SENTIMENT, CHECKS IF THIS IS EQUAL TO THE ONE
    # THE USER PASSES IN. FOR EXAMPLE, DOES THE STOCK CONTAIN A "BULLISH" SENTIMENT?
    # MEAN RATING UNDER 3 IS CONSIDERED A BUY/BULLISH, AND ABOVE 3 IS SELL/BEARISH
    def __contains__(self,sentiment):
        if self.mean < 3:
            feeling = "BULLISH"
        else:
            feeling = "BEARISH"
        if sentiment.upper() == feeling:
            return "TRUE, THIS STOCK IS {}".format(feeling.upper())
        else:
            return "FALSE, SENTIMENT IS {}".format(feeling.upper())

    # RETURNS THE RATING WITH THE MOST ANALYSTS
    def consensus(self):
        if None in self.ratings.values():
            return "RATINGS UNAVAILABLE"
        else:
            return max(self.ratings, key=self.ratings.get)

    # TAKES THE DIVIDEND YIELD AND CALCULATES THE APPROXIMATE ANNUAL DIVIDEND
    # PAYOUT (YIELD * CURRENT PRICE )
    def approx_dividend(self):
        if self.dividend != "None":
            div = float(self.dividend.replace("%", ""))
            return ("${}".format(round(self.price * (div / 100), 2)))
        else:
            return "None"

    # RETURNS ALL THE PRICE TARGETS IN A BULLET FORMAT
    def price_targets(self):
        if None in self.targets:
            return "TARGETS UNAVAILABLE"
        else:
            return ("PRICE TARGETS:\n * HIGH: ${}\n * LOW: ${}\n * MEDIAN: ${}".format(self.targets[1],
                                                                                       self.targets[2],
                                                                                       self.targets[0]))



# CREATES DICTIONARY ENTRY THAT IS CACHED AND PASSED INTO THE STOCK CLASS
def create_entry(bloom,cnn,reuters):
    entry = {}
    entry['name'] = bloom.find('h1', class_='companyName__99a4824b').text
    entry['price'] = float(bloom.find('span', class_='priceText__1853e8a5').text.replace(",",""))
    entry['dividend'] = find_dividend(bloom)
    entry['targets'] = find_targets(cnn)
    entry['volume'] = find_volume(bloom)
    consensus = find_ratings(reuters)
    entry['mean rating'] = consensus[1]
    entry['ratings'] = consensus[0]
    entry['cache_time'] = datetime.now().strftime(DATETIME_FORMAT)
    return entry

# RETRIEVES THE DIVIDEND YIELD % USING BLOOMBERG BEAUTIFULSOUP OBJECT
def find_dividend(soup):
    dividend = soup.find('span', text="Dividend").find_next('span').text
    if dividend == "--":
        return "None"
    else:
        return dividend


# FINDS PRICE TARGETS USING CNN BEAUTIFULSOUP OBJECT
def find_targets(soup):
    targets = []
    count = 0
    predictions = soup.find('div', class_='wsod_twoCol')
    predictions = predictions.find_next('p').text
    predictions = predictions.replace(",","")
    predictions = predictions.split()
    for x in range(len(predictions)):
        if count < 3:
            if "." in predictions[x]:
                if predictions[x][-1] == ".":
                    predictions[x] = predictions[x][:-1]
                try:
                    targets.append(float(predictions[x]))
                    count += 1
                except:
                    continue
    targets = [None, None, None] if len(targets) == 0 else targets
    return targets

# FINDS VOLUME USING BLOOMBERG BEAUTIFULSOUP OBJECT
def find_volume(soup):
    volume_section = soup.find('header', string="Volume")
    volume = volume_section.find_next('div').text
    return volume

# FINDS ANALYST RATINGS USING REUTERS BEAUTIFULSOUP OBJECT
# RETURNS A DICTIONARY CONTAINING NONEVALUES IF THERE ARE NO RATINGS
def find_ratings(soup):
    consensus = {}
    mean_rating = ""
    ratings = ["BUY", "OUTPERFORM", "HOLD", "UNDERPERFORM", "SELL", "No Opinion", "Mean Rating"]
    for rating in ratings:
        for x in soup.findAll('td'):
            if rating in x.text:
                if rating == "Mean Rating":
                    mean_rating = (float(x.find_next('td').text))
                else:
                    consensus[rating] = (int(x.find_next('td').text))
    if len(consensus) == 0:
        for rating in ratings:
            consensus[rating] = None
        mean_rating = None
    return (consensus,mean_rating)

# CHECKS THE TIMESPAMP FOR A TICKER IN THE CACHE. IF THE STOCK HAS BEEN IN
# FOR MORE THAN ONE DAY, THE PROGRAM RETRIEVED UP-TO-DATE INFO
def has_cache_expired(timestamp, expire_in_days):
    now = datetime.now()
    cache_timestamp = datetime.strptime(timestamp, DATETIME_FORMAT)
    delta = now - cache_timestamp
    delta_days = delta.days
    if delta_days >= expire_in_days:
        return True
    else:
        return False

# SOME TICKERS (LIKE RDS.A FOR SHELL CORPORATION) HAVE PERIODS IN THEIR TICKERS
# IF THIS IS THE CASE, IT ADJUSTS THE TICKER SO THAT IT MAY BE PASSES WITHOUT
# ERROR INTO EACH OF THE URLS
def check_ticker(ticker):
    tickers = {}
    tickers["bloom"] = ticker.replace(".","/")
    tickers["cnn"] = ticker.replace(".","")
    tickers["reuters"] = ticker.replace(".","")
    return tickers

# RUNS THREE REQUESTS AND CREATES BEAUTIFULSOUP OBJECTS FOR A TICKER
# RETURNS BOTH THE STOCK OBJECT AND DICTIONARY FORMAT FOR THE CACHE
def get_info(ticker):
    tickers = check_ticker(ticker)
    bloom_data = requests.get("https://www.bloomberg.com/quote/{}:US".format(tickers["bloom"])).text
    cnn_data = requests.get("http://money.cnn.com/quote/forecast/forecast.html?symb={}".format(tickers["cnn"])).text
    reuters_data = requests.get("https://www.reuters.com/finance/stocks/analyst/{}".format(tickers["reuters"])).text
    bloom_soup = BeautifulSoup(bloom_data, "html.parser")
    cnn_soup = BeautifulSoup(cnn_data, "html.parser")
    reuters_soup = BeautifulSoup(reuters_data, "html.parser")
    stock_entry = create_entry(bloom_soup,cnn_soup,reuters_soup)
    stock_info = Stock(stock_entry)
    return (stock_info,stock_entry)

# CHECKS IF CACHE EXISTS. IF NOT CREATE ONE AND RUNS THE PROGRAM FOR 5 STOCKS
# AUTOMATICALLY ENTERING THE INFORMATION INTO THE CACHE AND DATABASE
def begin():
    auto = ["AAPL","FB","XOM","AMZN","GOOGL"]
    try:
        with open("data.json") as f:
            cache = json.load(f)
    except:
        print("\nNO CACHE EXISTS - CREATING ONE WITH THE FOLLOWING ENTRIES...")
        print("APPLE (AAPL), FACEBOOK (FB), EXXON (XOM), AMAZON (AMZN), GOOGLE (GOOGL)\n")
        create_tables()
        with open("data.json", "w") as f:
            entry = {}
            for ticker in auto:
                stock = get_info(ticker)
                stock_obj = stock[0]
                insert_stock(stock_obj)
                entry[ticker] = stock[1]
            json.dump(entry, f)

# EITHER RETRIEVES STOCK INFO FROM THE CACHE, GENERATES A NEW ENTRY, OR UPDATES
# AN EXISTING ENTRY IF THE TIMESTAMP HAS EXPIRED
def retrieve_information(ticker, cache, testing=False):
    try:
        if ticker not in cache:
            if testing == False:
                print("##### NOT IN CACHE - CREATING STOCK ENTRY FOR {}.....".format(ticker))
            update = False
            stock = get_info(ticker)
            stock_obj = stock[0]
            stock_cache_entry = stock[1]
        elif has_cache_expired(cache[ticker]['cache_time'],1):
            if testing == False:
                print("##### GETTING MORE RECENT STOCK INFO FOR {}.....".format(ticker))
            update = True
            stock = get_info(ticker)
            stock_obj = stock[0]
            stock_cache_entry = stock[1]
        else:
            if testing == False:
                print("##### RETRIEVING STOCK INFROMATION FOR {} FROM CACHE.....".format(ticker))
            update = False
            stock_cache_entry = cache[ticker]
            stock_obj = Stock(stock_cache_entry)
    except:
        # IF ERROR WHEN RETRIEVING INFORMATION, RETURN "ERROR" FOR LATER USE
        return "Error"
    return (stock_obj,stock_cache_entry,update)

def print_basic(stock_obj):
    # PRINTS OUT BASIC INFORMATION ABOUT STOCK
    print("\n####################")
    print("NAME: {}".format(stock_obj.name))
    print("CURRENT PRICE: ${}".format(stock_obj.price))
    print("CONSENSUS: {}".format(stock_obj.consensus()))
    print("DIVIDEND YIELD: {}".format(stock_obj.dividend))
    print("APPROX ANNUAL DIVIDEND: {}".format(stock_obj.approx_dividend()))
    print(stock_obj.price_targets())


# IF NEEDED, WILL CACHE STOCK DICT AND ENTER/UPDATE INFO INTO THE DATABASE
def cache_or_db(ticker, stock_obj, stock_cache_entry, cache, update):
    if ticker not in cache:
        insert_stock(stock_obj)
        with open("data.json") as f:
            existing = json.load(f)
        existing[ticker] = stock_cache_entry
        with open("data.json", "w") as f:
            json.dump(existing,f)
    elif update:
        update_stock(stock_obj)
        with open("data.json") as f:
            existing = json.load(f)
        existing[ticker] = stock_cache_entry
        with open("data.json", "w") as f:
            json.dump(existing,f)

def run():
    print("\n")
    print("#####################################################################\n")
    print("WELCOME! THIS PROGRAM IS DESIGNED TO LOOK UP BASIC STOCK INFORMATION")
    print("FOR A PUBLIC COMPANY GIVEN THE STOCK TICKER (E.G. FB FOR FACEBOOK)")
    print("THE PROGRAM USES BEAUTIFULSOUP TO SCRAPE THREE DIFFERENT SITES FOR")
    print("VARIOUS INFORMATION (PRICE, VOLUME, FORECASTS, ETC.):\n")
    print(" * BLOOMBERG (BASIC INFO)")
    print(" * CNN MONEY (PRICE TARGETS)")
    print(" * REUTERS (ANALYSTS RECOMMENDATIONS)\n")
    print("FIRST, THE PROGRAM CHECKS IF THE TICKER IS IN THE DATA.JSON CACHE.")
    print("IF NOT, THE URL REQUESTS ARE MADE, INFORMATION SCRAPED, AND THEN")
    print("STORED AS A DICTIONARY ENTRY IN THE JSON FILE. INFORMATION IS CACHED")
    print("FOR ONE DAY (MARKETS FLUCTUATE FREQUENTLY). AT THE END, THE ANALYST")
    print("RECOMMENDATIONS AND PRICE TARGETS ARE GRAPHED USING PLOTLY. YOU MAY")
    print("RUN THE PROGRAM AS MANY TIMES AS YOU LIKE.\n")
    print("IT IS RECOMMENDED TO SEARCH FOR LARGER, WELL KNOWN COMPANIES AS THEIR")
    print("INFORMATION IS MORE LIKELY TO BE COVERED BY ANALYSTS. USE THE EXACT")
    print("TICKERS AS FOUND ON THE NYSE OR NASDAQ.\n")
    print("THE FOLLOWING STOCKS ALREADY EXIST IN THE CACHE AND DATABASE:")
    print(" * AAPL (APPLE)\n * FB (FACEBOOK)\n * XOM (EXXON)\n * AMZN (AMAZON)\n * GOOGL (ALPHABET)\n")
    print("SOME TICKERS THAT ARE NOT CACHED BY ARE KNOWN TO WORK INCLUDE:")
    print(" * MSFT (MICROSOFT)\n * MCD (MCDONALD'S)\n * DIS (DISNEY)\n * BABA (ALIBABA)\n")
    print("#####################################################################\n")

    with open("data.json") as f:
        cache = json.load(f)

    # RUNS THE LOOP AS MANY TIMES AS THE USER WISHES
    # HAS THE OPTION OF EITHER AUTOMATICALLY OPENEING A NEW BROWSER TAB TO
    # DISPLAY THE PLOTLY GRAPH, OR EXAMINE THE HTML FILE GENERATED
    ticker = input("##### PLEASE ENTER A TICKER: ").upper()
    ticker = ticker.replace(" ", "")
    while ticker != "EXIT":
        stock = retrieve_information(ticker,cache)
        if stock != "Error":
            print_basic(stock[0])
            cache_or_db(ticker, stock[0], stock[1], cache, stock[2])
            preference = input("\n##### VISUAL TO OPEN IN BROWSER AUTOMATICALLY? (TYPE YES OR NO): ").upper()
            if preference == "YES":
                create_visual(stock[0], ticker, False)
        else:
            print("##### COULD NOT RETRIEVE INFORMATION FOR GIVEN TICKER.")
            ticker = input("\n##### TRY ANOTHER TICKER, OR TYPE 'EXIT' TO EXIT: ").upper()
            ticker = ticker.replace(" ", "")
            continue
        ticker = input("\n##### ENTER ANOTHER TICKER, OR TYPE 'EXIT' TO EXIT: ").upper()
        ticker = ticker.replace(" ", "")


if __name__ == "__main__":
    begin()
    run()
