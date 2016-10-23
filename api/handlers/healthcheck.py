from tornado.web import RequestHandler

#Only purpose of this handler is to be able to tell if the service is alive
class HealthCheckHandler(RequestHandler):

    def get(self):
        self.write("I'm alive")
