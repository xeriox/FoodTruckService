import unittest

from api.handlers.helpers import FilterToQueryParser
from api.repositories.base import GPSPointCriteria, Query, StringCriteria


class HelperFilterPaserTestCase(unittest.TestCase):

    def test_location_criteria_parsing_positive(self):

        parser = FilterToQueryParser(Query())

        gps_point_criteria = parser.parse_and_append_criteria(
            criteria=GPSPointCriteria(),
            comparator="nearby:1000",
            value="-85.1231,140.12321321"
        )

        self.assertTrue(gps_point_criteria.near_by["distance"] == 1000)
        self.assertTrue(gps_point_criteria.near_by["latitude"] == -85.1231)
        self.assertTrue(gps_point_criteria.near_by["longitude"] == 140.12321321)

        parser = FilterToQueryParser(Query())

        string_criteria = parser.parse_and_append_criteria(
            criteria=StringCriteria(),
            comparator="contain",
            value="contain_value"
        )

        self.assertTrue(string_criteria.contain == "contain_value")

    def test_location_criteria_parsing_negative(self):

        parser = FilterToQueryParser(Query())

        self.failUnlessRaises(TypeError,
            parser.parse_and_append_criteria,
                criteria=GPSPointCriteria(),
                comparator="nearby:1000",
                value="-185.1231,140.12321321"
            )

        self.failUnlessRaises(TypeError,
            parser.parse_and_append_criteria,
                criteria=GPSPointCriteria(),
                comparator="nearby:1000",
                value="185.1231,140.12321321"
            )

        self.failUnlessRaises(TypeError,
            parser.parse_and_append_criteria,
                criteria=GPSPointCriteria(),
                comparator="nearby:1000",
                value="-85.1231,-190.12321321"
            )

        self.failUnlessRaises(TypeError,
            parser.parse_and_append_criteria,
                criteria=GPSPointCriteria(),
                comparator="nearby:1000",
                value="-85.1231,190.12321321"
            )

        self.failUnlessRaises(TypeError,
            parser.parse_and_append_criteria,
                criteria=GPSPointCriteria(),
                comparator="nearby",
                value="-85.1231,90.12321321"
            )

        self.failUnlessRaises(TypeError,
            parser.parse_and_append_criteria,
                criteria=GPSPointCriteria(),
                comparator="nearby:1000",
                value="-85.1231;90.12321321"
            )

    def test_filter_to_query_parsing_positive(self):

        base_query = Query()

        base_query.location = GPSPointCriteria()
        base_query.food_items = StringCriteria()

        filter_parser = FilterToQueryParser(base_query)

        filter = '[' \
                     '{"property" : "location", "comparator" : "nearby:1000", "value" : "-85.1231,140.12321321"},' \
                     '{"property" : "food_items", "comparator" : "contain", "value" : "contain_value"}' \
                     ']'


        base_query = filter_parser.parse_and_append_filter_to_query(filter)

        self.assertTrue(base_query)

        self.assertTrue(base_query.location, "Location is not set %s" % base_query.__dict__)

        self.assertTrue(isinstance(base_query.location,GPSPointCriteria),"Location was not of instance GPSPointCriteria")
        self.assertTrue(isinstance(base_query.food_items, StringCriteria),
                        "food_items was not of instance StringCriteria")

        self.assertTrue(base_query.location.near_by["latitude"] == -85.1231)
        self.assertTrue(base_query.location.near_by["longitude"] == 140.12321321)
        self.assertTrue(base_query.location.near_by["distance"] == 1000)
        self.assertTrue(base_query.food_items.contain == "contain_value")

        base_query = Query()

        base_query.location = GPSPointCriteria()
        base_query.food_items = StringCriteria()

        filter_parser = FilterToQueryParser(base_query)

        filter = '[{"property" : "location", "comparator" : "nearby:1000", "value" : "-85.1231,140.12321321"}]'

        base_query = filter_parser.parse_and_append_filter_to_query(filter)

        self.assertTrue(base_query.location.near_by["latitude"] == -85.1231)
        self.assertTrue(base_query.location.near_by["longitude"] == 140.12321321)
        self.assertTrue(base_query.location.near_by["distance"] == 1000)
        self.assertTrue(base_query.food_items.contain == None)

    def test_filter_to_query_parsing_negative(self):

        base_query = Query()

        base_query.location = GPSPointCriteria()

        filter_parser = FilterToQueryParser(base_query)

        filter = '[{"property" : "location", "comparator" : "nearby:1000", "value" : "-85.1231,140.12321321]'

        self.failUnlessRaises(TypeError,
                              filter_parser.parse_and_append_filter_to_query,filter
            )

        filter = '[{"comparator" : "nearby:1000", "value" : "-85.1231,140.12321321"}]'

        self.failUnlessRaises(TypeError,
                              filter_parser.parse_and_append_filter_to_query,filter
            )

        filter = '[{"property" : "location", "value" : "-85.1231,140.12321321"}]'

        self.failUnlessRaises(TypeError,
                              filter_parser.parse_and_append_filter_to_query,filter
            )

        filter = '[{"property" : "location", "comparator" : "nearby:1000"}]'

        self.failUnlessRaises(TypeError,
                              filter_parser.parse_and_append_filter_to_query,filter
            )