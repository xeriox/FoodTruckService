import json

from tornado.options import options
from api.repositories.base import BaseRepository,Query, GPSPoint, StringCriteria, GPSPointCriteria
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search


class FoodTruckRepository(BaseRepository) :

    elastic_search_client = None

    def __init__(self):
       # URL is configured in main by tornado.options.define
       self.elastic_search_client = Elasticsearch(
        [options.elasticsearch_url]
       )

    # Storing foodtruck model in underlying datastore
    def create(self,model):

        self.elastic_search_client.index(
            index='foodtrucks',
            doc_type='foodtruck-type',
            body=self.map_from_model_to_es(model),
            id=model.id
        )

    # Querying foodtruck models in underlying datastore
    def findByQuery(self,query):

        s = Search(using=self.elastic_search_client , index="foodtrucks").query("match_all")

        if query.location.near_by:
            s = s.filter("geo_distance",
                    distance="%sm" % query.location.near_by["distance"],
                    location={
                        "lat": query.location.near_by["latitude"],
                        "lon": query.location.near_by["longitude"]
                    }
                    )

        if query.food_items.contain:
            s = s.filter("wildcard",
                    food_items="*%s*" % query.food_items.contain.lower()
                    )

        return [self.map_from_es_to_model(model) for model in s[query.offset:query.offset+query.limit].execute()]

    def map_from_es_to_model(self,es_model):

        return FoodTruckModel(
            name=es_model.name,
            location=GPSPoint(float(es_model.location.lat),float(es_model.location.lon)),
            location_description = es_model.location_description,
            opening_hours = es_model.opening_hours,
            food_items=es_model.food_items,
            id=es_model.meta.id
        )

    def map_from_model_to_es(self, model):

        return json.dumps({
            'name': model.name,
            'food_items' : model.food_items,
            'opening_hours' : model.opening_hours,
            'location_description' : model.location_description,
            'location' : {
                'lat' : model.location.latitude,
                'lon' : model.location.longitude
            }
        })

class FoodTruckQuery(Query):

    name = StringCriteria()
    food_items = StringCriteria()
    location = GPSPointCriteria()

    def __init__(self):
        self.name = StringCriteria()
        self.food_items = StringCriteria()
        self.location = GPSPointCriteria()


class FoodTruckModel:
    id = None
    name = None
    location = None
    food_items = None
    opening_hours = None
    location_description = None

    def __init__(self,id=None,name=None,location=None,food_items="",opening_hours="",location_description=""):
        self.id = id
        self.name = name
        self.location = location
        self.food_items = food_items
        self.opening_hours = opening_hours
        self.location_description = location_description