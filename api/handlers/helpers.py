import json

from api.repositories.base import GPSPointCriteria, StringCriteria


class FilterToQueryParser:

    def __init__(self, base_query):

        # Initializing specialized parsers based on criteria type
        self.parsing_functions = {
            StringCriteria: self.parse_and_append_to_string_criteria,
            GPSPointCriteria : self.parse_and_append_to_gpspoint_criteria
        }
        self.query = base_query

    # This function receive a filter, and parse and append it to base_query provided in the constructur
    def parse_and_append_filter_to_query(self,filter):

        # If there is no filter we just return the current query
        if not filter :
            return self.query

        filter_array = []

        # It's required that the filter is an json object
        try:
            filter_array = json.loads(filter)
        except ValueError:
            raise TypeError("Provided filter is not a valid json object")

        # For each filter object in provided filters we parse it and append it the query
        for criteria in filter_array:

            property = criteria.setdefault("property", None)

            if not property:
                raise TypeError("Property for criteria is not set")

            # Getting the current criteria from the base query, parse and replace it the updated one
            setattr(self.query,property,self.parse_and_append_criteria(
                getattr(self.query,property),
                criteria.setdefault("comparator", None),
                criteria.setdefault("value", None)
            ))

        return self.query

    def parse_and_append_criteria(self,criteria,comparator,value):

        if not (comparator and value):
            raise TypeError("A valid filter criteria consist of a property, a comparator and a value")

        # Based on criteria type, we use the specialized parser
        return self.parsing_functions[criteria.__class__](criteria,comparator,value)

    # Parse string filters
    def parse_and_append_to_string_criteria(self,criteria,comparator,value):

        if "contain" in comparator:
            criteria.set_contain(value)

        return criteria
    # Parse GPS Pount filter
    def parse_and_append_to_gpspoint_criteria(self,criteria,comparator,value):

        # Validate if the comparator is supported by this type of criteria
        if not "nearby" in comparator:
            raise TypeError("comparator %s is not supported for gpspoint" % comparator)

        gps_coordinates = value.split(',')

        # We check if the gps coordinates are in the correct format
        if not len(gps_coordinates) == 2:
            raise TypeError("GPS Coordinate incorrect value correct format is latitude,longitude")

        latitude = float(gps_coordinates[0])
        longitude = float(gps_coordinates[1])

        near_by = comparator.split(':')

        # Validate the correct usage of nearby comparator
        if not len(near_by) == 2:
            raise TypeError("nearby comparator is not used correct, correct usage is by an example nearby:1000")

        distance = int(near_by[1])

        criteria.set_near_by(latitude,longitude,distance)

        return criteria



