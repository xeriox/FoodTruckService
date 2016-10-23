import pprint

import requests
from tornado.options import define

from api.repositories.base import GPSPoint
from api.repositories.foodtruck import FoodTruckRepository, FoodTruckModel

if __name__ == "__main__":
    define("elasticsearch_url",
           default="https://search-foodtruck-biviy6zrdphmaqstkngtyyipky.eu-west-1.es.amazonaws.com:443",
           help="Elastich Search URL")

    repo = FoodTruckRepository()

    response = requests.get('https://data.sfgov.org/resource/6a9r-agq8.json')

    for item in response.json():

        name = item.setdefault("applicant", "Uknown")
        food_items = item.setdefault("fooditems", "")
        id = item.setdefault("objectid", None)
        opening_hours = item.setdefault("dayshours","")
        location_description = item.setdefault("locationdescription","")
        location = None

        latitude = item.setdefault("latitude", None)
        longitude = item.setdefault("longitude", None)

        if latitude and longitude:
            location = GPSPoint(latitude=float(latitude),longitude=float(longitude))

        repo.create(FoodTruckModel(id=id,name=name, food_items=food_items,location=location,opening_hours=opening_hours,location_description=location_description))