import tornado.gen, tornado.ioloop, tornado.web, tornado.websocket


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        paragraphs = [
                'Process Dynamics Engine API Reference:',
                'GET /models/all: list all models',
                'POST /models/{model_id}: create a new simulation',
                'GET /sims/all: list all active simulations',
                'GET /sims/{sim_id}: get simulation status',
                'GET /sims/{sim_id}/{tag_id}: get tag status'
        ]
        self.write('<p>' + '</p><p>'.join(paragraphs) + '</p>')


class ModelListHandler(tornado.web.RequestHandler):

    def get(self):
        pass


class ModelCreateHandler(tornado.web.RequestHandler):

    def post(self, model_id):
        pass


class SimulationListHandler(tornado.web.RequestHandler):

    def get(self):
        pass


class SimulationGetHandler(tornado.web.RequestHandler):

    def get(self, sim_id):
        pass


class TagGetHandler(tornado.web.RequestHandler):

    def get(self, sim_id, tag_id):
        pass


class WebSocketHandler(tornado.websocket.WebSocketHandler):

    def check_origin(self, origin):
        # Allow access from local development server.
        if origin == 'file://':
            return True
        return False

    def open(self, socket_id):
        pass

    def on_message(self, message):
        pass

    def on_close(self):
        pass


def make_app():
    return tornado.web.Application([
        (r'/', MainHandler),
        (r'/models/all/?', ModelListHandler),
        (r'/models/(\d+)/?', ModelCreateHandler),
        (r'/sims/all/?', SimulationListHandler),
        (r'/sims/(\d+)/?', SimulationGetHandler),
        (r'/sims/(\d+)/(\d+)/?', TagGetHandler),
        (r'/([0-9a-f\-]+)', WebSocketHandler)
    ])


if __name__ == '__main__':
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
