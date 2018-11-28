import uuid
import tornado.gen, tornado.ioloop, tornado.web, tornado.websocket
from models import Model, Session, Simulation


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
        session = Session()
        try:
            socket_id = str(uuid.uuid4())
            sim = Simulation(model_id=model_id, socket_id=socket_id)
            session.add(sim)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()


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
    # TODO: this is temporary code to initialize the available models
    session = Session()
    try:
        f = open('wood_berry.pkl', 'rb')
        pickled_model = pickle.load(f)
        session.add(Model(
                name='Wood-Berry Distillation',
                system=pickled_model.system,
                inputs=pickled_model.inputs,
                outputs=pickled_model.outputs))
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        f.close()
        session.close()

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
