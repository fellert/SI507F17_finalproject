import unittest
import json
from final import *

class TestStock(unittest.TestCase):

    def setUp(self):
        try:
            with open("data.json") as f:
                self.cache = json.load(f)
            request = self.cache['MCD']
        except:
            request = get_info('MCD')
            self.stock = request[0]

    def test_consensus(self):
        self.assertEqual(self.stock.consensus(),max(self.stock.ratings, key=self.stock.ratings.get))


class TestAuto(unittest.TestCase):

    def setUp(self):
        begin()
        self.cache = open("data.json")

    def test_cache_exists(self):
        self.assertTrue(json.load(self.cache))

    def test_cache_contents(self):
        self.assertEqual(len(json.load(self.cache)), 5)

    def tearDown(self):
        self.cache.close()



if __name__ == '__main__':
    unittest.main(verbosity=2)
