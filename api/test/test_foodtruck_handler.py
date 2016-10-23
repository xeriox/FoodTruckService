import unittest

from api.handlers.helpers import FilterToQueryParser
from api.repositories.base import GPSPointCriteria, StringCriteria
from api.repositories.foodtruck import FoodTruckQuery


class FoodTruckFilterPaserTestCase(unittest.TestCase):

    def test_foodtruck_query_parsing(self):

        filter_parser = FilterToQueryParser(FoodTruckQuery())

        filter = '[' \
                     '{"property" : "location", "comparator" : "nearby:1000", "value" : "-85.1231,140.12321321"},' \
                     '{"property" : "food_items", "comparator" : "contain", "value" : "contain_value"}' \
                     ']'


        query = filter_parser.parse_and_append_filter_to_query(filter)

        self.assertTrue(query)

        self.assertTrue(query.location, "Location is not set %s" % query.__dict__)

        self.assertTrue(isinstance(query.location,GPSPointCriteria),"Location was not of instance GPSPointCriteria")
        self.assertTrue(isinstance(query.food_items, StringCriteria),
                        "food_items was not of instance StringCriteria")

        self.assertTrue(query.location.near_by["latitude"] == -85.1231)
        self.assertTrue(query.location.near_by["longitude"] == 140.12321321)
        self.assertTrue(query.location.near_by["distance"] == 1000)
        self.assertTrue(query.food_items.contain == "contain_value")