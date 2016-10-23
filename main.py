import os
from tornado.options import define

import tornado.ioloop
from tornado.web import RequestHandler

from api.handlers import foodtruck
from api.handlers import healthcheck
import os

define("elasticsearch_url", default=os.environ["ELASTICSEARCHURL"], help="Elastich Search URL")

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
}

class IndexHandler(RequestHandler):
	def get(self):
		self.render("static/index.html")

def make_app():
    return tornado.web.Application([
        (r"/",IndexHandler),
        (r"/api/foodtrucks", foodtruck.FoodTruckHandler),
        (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': './static'}),
        (r"/health_check/" ,healthcheck.HealthCheckHandler)

    ],**settings)

if __name__ == "__main__":
    app = make_app()
    app.listen(80)
    tornado.ioloop.IOLoop.current().start()
