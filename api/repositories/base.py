

# Base repository, ensuring all reposistories comply to the same interface
class BaseRepository:

    def getById(self, id):
        pass

    def findByQuery(self,query):
        pass

    def update(self,id,model):
        pass

    def create(self,model):
        pass

    def delete(self,model):
        pass

#Class for holding GPS location data
class GPSPoint:

    latitude = None
    longitude = None

    def __init__(self,latitude, longitude):

        if -90 > latitude or latitude > 90:
            raise TypeError("Invalid latitude correct latitude is between -90 and 90, yours are: %s" % latitude)

        if -180 > longitude or longitude > 180:
            raise TypeError("Invalid longitude correct longitude is between -90 and 90, yours are: %s" % longitude)

        self.latitude = latitude
        self.longitude = longitude

    @staticmethod
    def parse_from_string(string, delimiter = ","):
        location = string.split(delimiter)

        return GPSPoint(float(location[0]),float(location[1]))

#Base Query ensuring that all queries comply to the same interface
class Query:
    offset = None
    limit = None

    pass

#String Criteria model for general query usage
class StringCriteria:

    contain = None

    def set_contain(self,string):
        self.contain = string
        return self

# GPS Point Criteria model for general query usage
class GPSPointCriteria:

    near_by = None

    def set_near_by(self,latitude,longitude,distance):

        if -90.0 > latitude or latitude > 90.0:
            raise TypeError("Invalid latitude correct latitude is between -90 and 90, yours are: %s" % latitude)

        if -180.0 > longitude or longitude > 180.0:
            raise TypeError("Invalid longitude correct longitude is between -90 and 90, yours are: %s" % longitude)

        self.near_by = {
            'longitude' : longitude,
            'latitude' : latitude,
            'distance'  : distance
        }

        return self