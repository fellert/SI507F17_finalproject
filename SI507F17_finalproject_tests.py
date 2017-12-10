import unittest
import psycopg2
from visualize import *
from SI507F17_finalproject import *
from database import *

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

    def setUp(self):
        with open("data.json") as f:
            self.cache = json.load(f)
        self.request = retrieve_information('MCD', self.cache, True)
        self.request2 = retrieve_information('GELYF', self.cache, True)
        self.request3 = retrieve_information('DL', self.cache, True)
        self.mcd = self.request[0]
        self.gelyf = self.request2[0]
        self.dl = self.request3[0]
        create_visual(self.mcd, 'MCD', True)
        self.visual = open("MCD_info.html")
        cache_or_db('MCD', self.mcd, self.request[1], self.cache, self.request[2])
        cache_or_db('GELYF', self.gelyf, self.request2[1], self.cache, self.request2[2])
        cache_or_db('DL', self.dl, self.request3[1], self.cache, self.request3[2])

    def test_name(self):
        self.assertEqual(self.mcd.name, "McDonald's Corp")
        self.assertEqual(self.gelyf.name, "Geely Automobile Holdings Ltd")
        self.assertEqual(self.dl.name, "China Distance Education Holdings Ltd")
        self.assertIsInstance(self.mcd.price, float)
        self.assertIsInstance(self.mcd.dividend, str)

    def test_ratings(self):
        for rating in self.mcd.ratings:
            self.assertIsInstance(self.mcd.ratings[rating], int)
        for rating in self.dl.ratings:
            self.assertEqual(self.dl.ratings[rating], None)

    def test_targets(self):
        for target in self.mcd.targets:
            self.assertIsInstance(target, float)
        for target in self.gelyf.targets:
            self.assertEqual(target, None)

    def test_dividend(self):
        float_yield = float(self.mcd.dividend.replace("%", ""))
        div = round(self.mcd.price * (float_yield / 100), 2)
        self.assertEqual(self.mcd.approx_dividend(), "${}".format(div))

    def test_consensus(self):
        self.assertEqual(self.mcd.consensus(),max(self.mcd.ratings, key=self.mcd.ratings.get))

    def test_repr(self):
        name = self.mcd.name
        price = self.mcd.price
        self.assertEqual(repr(self.mcd), "The most recent price for {} is ${}".format(name,price))

    def test_visual_file(self):
        self.assertTrue(self.visual.read())

    def test_timestamp(self):
        stamp = self.request[1]['cache_time']
        now = datetime.now()
        cache_timestamp = datetime.strptime(stamp, DATETIME_FORMAT)
        delta = now - cache_timestamp
        delta_in_days = delta.days
        self.assertTrue(delta_in_days < 1)

    def test_contains(self):
        self.assertEqual(self.mcd.__contains__("BULLISH"), "TRUE, THIS STOCK IS BULLISH")

    def tearDown(self):
        self.visual.close()

class TestDatabase(unittest.TestCase):

    def setUp(self):
        with open("data.json") as f:
            self.cache = json.load(f)
        self.request = retrieve_information('MCD', self.cache, True)
        self.mcd = self.request[0]
        cache_or_db('MCD', self.mcd, self.request[1], self.cache, self.request[2])

    def test_company_table(self):
        cur.execute("SELECT name FROM Company")
        names = cur.fetchall()
        names = [x[0] for x in names]
        self.assertTrue(self.mcd.name in names)

    def test_targets_table(self):
        cur.execute("SELECT median, high, low FROM Targets WHERE \
                     Targets.stock_id = (SELECT Company.id from Company WHERE Company.name = %s)",
                     (self.mcd.name,))
        targets = cur.fetchall()
        targets = targets[0]
        self.assertEqual(self.mcd.targets[0], targets[0])
        self.assertEqual(self.mcd.targets[1], targets[1])
        self.assertEqual(self.mcd.targets[2], targets[2])

    def test_info_table(self):
        cur.execute("SELECT price, volume, consensus, dividend_yield \
                     FROM Info WHERE Info.stock_id = (SELECT Company.id from Company WHERE Company.name = %s)",
                     (self.mcd.name,))
        info = cur.fetchall()
        info = info[0]
        self.assertTrue(self.mcd.price, info[0])
        self.assertTrue(self.mcd.volume, info[1])
        self.assertTrue(self.mcd.consensus, info[2])
        self.assertTrue(self.mcd.dividend, info[3])

    def test_ratings_table(self):
        cur.execute("SELECT * FROM Ratings WHERE Ratings.stock_id = (SELECT Company.id from Company WHERE Company.name = %s)",
                     (self.mcd.name,))
        ratings = cur.fetchall()
        ratings = ratings[0][2:]
        count = 0
        for key in self.mcd.ratings:
            self.assertEqual(self.mcd.ratings[key], ratings[count])
            count += 1

class TestUnkown(unittest.TestCase):

    def setUp(self):
        with open("data.json") as f:
            self.cache = json.load(f)
        self.request = retrieve_information('NON_EXISTENT_TICKER', self.cache, True)

    def test_unkown_ticker(self):
        self.assertEqual(self.request, "Error")

if __name__ == '__main__':
    unittest.main(verbosity=2)
