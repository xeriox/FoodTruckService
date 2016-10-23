from tornado.web import RequestHandler

from api.handlers.helpers import FilterToQueryParser
from api.repositories.foodtruck import FoodTruckModel, FoodTruckRepository, FoodTruckQuery
import json

import pprint

class FoodTruckHandler(RequestHandler):

    # Mapping the foodtruck model to dictionary for easier jsonfy
    @staticmethod
    def modelTodict(model):

        return {
            'id' : model.id,
            'name': model.name,
            'food_items' : model.food_items,
            'opening_hours': model.opening_hours,
            'location_description': model.location_description,
            'location' : {
                'latitude' : model.location.latitude,
                'longitude' : model.location.longitude
            },
        }

    # Since all content providers in this service is producing json, we Content-Type to application/json
    def set_default_headers(self):
        self.set_header('Content-Type', 'application/json')


    def get(self):

        query = FoodTruckQuery()

        query.limit = int(self.get_argument('limit', 1000, True))
        query.offset = int(self.get_argument('offset', 0, True))

        try:
            query = FilterToQueryParser(query)\
                .parse_and_append_filter_to_query(self.get_argument('filter',None,True))

        except TypeError, e:
            self.clear()
            self.set_status(400)
            self.finish(json.dumps({'error' : str(e)}))

        query_results = FoodTruckRepository().findByQuery(query)

        self.write(json.dumps([FoodTruckHandler.modelTodict(o) for o in query_results]))