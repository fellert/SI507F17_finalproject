import unittest
import psycopg2
from visualize import *
from SI507F17_finalproject import *
from database import *

# THIS CLASS IS RUN FIRST AND TESTS IF THE BEGIN() METHOD RUNS THE AUTOMATIC
# SCRIPT TO CREATE 5 STOCK OBJECTS AND CACHE THEM
class TestAuto(unittest.TestCase):

    def setUp(self):
        begin()
        self.cache = open("data.json")

    def test_cache_exists(self):
        self.assertTrue(json.load(self.cache))

    def test_cache_contents(self):
        cache_dict = json.load(self.cache)
        for ticker in ["AAPL", "AMZN", "XOM", "GOOGL", "FB"]:
            self.assertTrue(ticker in cache_dict.keys())

    def tearDown(self):
        self.cache.close()

class TestClass(unittest.TestCase):
    # CREATES THREE STOCK REQUESTS AND OBJECTS, AND CACHES THEM AT THE END
    # AFTER THE FIRST SETUP() IS RUNVTHE SYSTEM WILL JUST PULL THE INFO FROM THE CACHE
    def setUp(self):
        with open("data.json") as f:
            self.cache = json.load(f)
        self.request = retrieve_information('MCD', self.cache, True)
        self.request2 = retrieve_information('GELYF', self.cache, True)
        self.request3 = retrieve_information('DL', self.cache, True)
        self.mcd = self.request[0]
        self.gelyf = self.request2[0]
        self.dl = self.request3[0]
        cache_or_db('MCD', self.mcd, self.request[1], self.cache, self.request[2])
        cache_or_db('GELYF', self.gelyf, self.request2[1], self.cache, self.request2[2])
        cache_or_db('DL', self.dl, self.request3[1], self.cache, self.request3[2])

    # TEST STOCK() CONSTRUCTOR - NAME, PRICE, IF THE PRICE/DIVIDEND IS THE RIGHT TYPE
    def test_constructor(self):
        self.assertEqual(self.mcd.name, "McDonald's Corp")
        self.assertEqual(self.gelyf.name, "Geely Automobile Holdings Ltd")
        self.assertEqual(self.dl.name, "China Distance Education Holdings Ltd")
        self.assertIsInstance(self.mcd.price, float)
        self.assertIsInstance(self.mcd.dividend, str)

    # ALL RATINGS FOR MCD SHOULD BE INTEGERS. DL DOES NOT HAVE ANY ANYALYST
    # RATINGS, SO THIS TESTS IF THE SYSTEM CORRECTLY INPUTS "NONE" FOR THOSE VALUES
    def test_ratings(self):
        for rating in self.mcd.ratings:
            self.assertIsInstance(self.mcd.ratings[rating], int)
        for rating in self.dl.ratings:
            self.assertEqual(self.dl.ratings[rating], None)

    # ALL MCD TARGETS SHOULD BE FLOATS. GELYF DOES NOT HAVE ANY PRICE TARGETS,
    # SO THIS TESTS IF THE SYSTEM CORRECTLY INPUTS "NONE" FOR THOSE VALUES
    def test_targets(self):
        for target in self.mcd.targets:
            self.assertIsInstance(target, float)
        for target in self.gelyf.targets:
            self.assertEqual(target, None)

    # TESTS THE MATH BEHIND THE APPROX_DIVIDEND METHOD
    def test_dividend(self):
        float_yield = float(self.mcd.dividend.replace("%", ""))
        div = round(self.mcd.price * (float_yield / 100), 2)
        self.assertEqual(self.mcd.approx_dividend(), "${}".format(div))

    # TESTS IF THE CONSENSUS METHOD ACTUALLY SELECTS THE RATING WITH THE MOST ANYALYST
    def test_consensus(self):
        self.assertEqual(self.mcd.consensus(),max(self.mcd.ratings, key=self.mcd.ratings.get))

    # TESTS IF THE REPR METHOD PRODUCES THE EXPECTED STRING
    def test_repr(self):
        name = self.mcd.name
        price = self.mcd.price
        self.assertEqual(repr(self.mcd), "The most recent price for {} is ${}".format(name,price))

    # TESTS THE TIMESTAMP/EXIRATION METHOD - ALL TIMESTAMPS, WHEN CONVERTING TO DELTA.DAYS
    # SHOULD BE LESS THAN 1
    def test_timestamp(self):
        stamp = self.request[1]['cache_time']
        now = datetime.now()
        cache_timestamp = datetime.strptime(stamp, DATETIME_FORMAT)
        delta = now - cache_timestamp
        delta_in_days = delta.days
        self.assertTrue(delta_in_days < 1)

    # TESTS IF THE CONTAINS METHOD CONVERTS THE MEAN RATING INTO THE CORRECT SENTIMENT
    def test_contains(self):
        self.assertEqual(self.mcd.__contains__("BULLISH"), "TRUE, THIS STOCK IS BULLISH")


class TestDatabase(unittest.TestCase):

    # CREATES A REQUEST AND OBJECT FOR ALIBABA. CACHES THIS INFORMATION
    # AND ENTERS IT INTO THE DATABASE
    def setUp(self):
        with open("data.json") as f:
            self.cache = json.load(f)
        self.request = retrieve_information('BABA', self.cache, True)
        self.baba = self.request[0]
        cache_or_db('BABA', self.baba, self.request[1], self.cache, self.request[2])

    # CHECKS IF THE COMPANY NAME MATCHES ANY IN THE "COMPANIES" TABLE
    def test_company_table(self):
        cur.execute("SELECT name FROM Company")
        names = cur.fetchall()
        names = [x[0] for x in names]
        self.assertTrue(self.baba.name in names)

    #  TESTS IF THE TARGET ENTRIES IN THE DB MATCH THOSE OF THE RESPECTIVE OBJECT
    def test_targets_table(self):
        cur.execute("SELECT median, high, low FROM Targets WHERE \
                     Targets.stock_id = (SELECT Company.id from Company WHERE Company.name = %s)",
                     (self.baba.name,))
        targets = cur.fetchall()
        targets = targets[0]
        self.assertEqual(self.baba.targets[0], targets[0])
        self.assertEqual(self.baba.targets[1], targets[1])
        self.assertEqual(self.baba.targets[2], targets[2])

    # TESTS IF THE BASIC INFO IN THE DB MATCHES THAT OF THE RESPECTIVE OBJECT
    def test_info_table(self):
        cur.execute("SELECT price, volume, consensus, dividend_yield \
                     FROM Info WHERE Info.stock_id = (SELECT Company.id from Company WHERE Company.name = %s)",
                     (self.baba.name,))
        info = cur.fetchall()
        info = info[0]
        self.assertTrue(self.baba.price, info[0])
        self.assertTrue(self.baba.volume, info[1])
        self.assertTrue(self.baba.consensus, info[2])
        self.assertTrue(self.baba.dividend, info[3])

    # TESTS IF THE RATINGS (BUY, SELL, HOLD, ETC.) MATCH THOSE OF THE RESPECTIVE OBJECT
    def test_ratings_table(self):
        cur.execute("SELECT * FROM Ratings WHERE Ratings.stock_id = (SELECT Company.id from Company WHERE Company.name = %s)",
                     (self.baba.name,))
        ratings = cur.fetchall()
        ratings = ratings[0][2:]
        count = 0
        for key in self.baba.ratings:
            self.assertEqual(self.baba.ratings[key], ratings[count])
            count += 1

# THIS CLASS TESTS AN EDGE CASE IF THE USER TYPES IN A NON-EXISTENT STOCK TICKER
# IT IS ITS OWN CLASS SO THAT THE REQUEST ONLY HAS TO BE MADE ONCE, AS THE PROGRAM
# CANNOT CACHE ANYTHING (NO DATA - RUNS INTO AN ERROR)
class TestUnkown(unittest.TestCase):

    def setUp(self):
        with open("data.json") as f:
            self.cache = json.load(f)
        self.request = retrieve_information('NON_EXISTENT_TICKER', self.cache, True)

    def test_unkown_ticker(self):
        self.assertEqual(self.request, "Error")

# SEPARATE CLASS TO TEST IF THE CREATE_VISUAL FUNCTION ACTUALLY CREATE AN HTML FILE
# IT IS ITS OWN CLASS SO THAT THE CREATE_VISUAL FUNCTION IS ONLY RUN ONCE (FOR A SINGLE TEST)
class TestVisualization(unittest.TestCase):
    def setUp(self):
        with open("data.json") as f:
            self.cache = json.load(f)
        self.request = retrieve_information('DIS', self.cache, True)
        self.dis = self.request[0]
        create_visual(self.dis, 'DIS', True)
        self.visual = open("DIS_info.html")

    # TESTS IF THE CREATE_VISUAL FUNCTION ACTUALLY CREATES AN HTML FILE
    def test_visual_file(self):
        self.assertTrue(self.visual.read())

    def tearDown(self):
        self.visual.close()


if __name__ == '__main__':
    unittest.main(verbosity=2)
