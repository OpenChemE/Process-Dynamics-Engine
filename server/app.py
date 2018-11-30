import json, pickle, uuid
import tornado.gen, tornado.ioloop, tornado.web, tornado.websocket
import sqlalchemy.orm.exc
from models import Model, Session, Simulation
from work import create_simulation


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
            q = session.query(Model) \
                       .filter_by(id=model_id) \
                       .with_for_update().one()
            data = pickle.dumps(
                    create_simulation(q.system, q.name, q.inputs, q.outputs))
            sim = Simulation(
                    model_id=model_id,
                    socket_id=socket_id,
                    locked=False,
                    data=data)
            session.add(sim)
            session.flush()
            session.commit()
            self.write(json.dumps({
                'status': 'success',
                'sim_id': sim.id,
                'model_id': model_id,
                'socket_id': socket_id,
            }))
        except sqlalchemy.orm.exc.NoResultFound:
            self.set_status(404)
            self.write(json.dumps({
                'status': 'error',
                'error': f'no model found',
            }))
            session.rollback()
        except sqlalchemy.orm.exc.MultipleResultsFound:
            self.set_status(500)
            self.write(json.dumps({
                'status': 'error',
                'error': f'multiple models found',
            }))
            session.rollback()
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({
                'status': 'error',
                'error': str(e),
            }))
            session.rollback()
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

    def send(self, message):
        if self.sim_id == None:
            print(f'Sent to socket {self.socket_id}: {message}')
        else:
            print(f'Sent to sim {self.sim_id}: {message}')
        self.write_message(message)

    def receive(self, message):
        if self.sim_id == None:
            print(f'Received from socket {self.socket_id}: {message}')
        else:
            print(f'Received from sim {self.sim_id}: {message}')

    def check_origin(self, origin):
        # Allow access from local development server.
        if origin == 'file://':
            return True
        return False

    def open(self, socket_id):
        self.sim_id = None
        self.socket_id = socket_id

        session = Session()
        try:
            q = session.query(Simulation) \
                       .filter_by(socket_id=self.socket_id) \
                       .with_for_update().one()
            if q.locked:
                self.send(f'Error: simulation {q.id} is currently locked. '
                        + 'Another user may be connected at the same time.')
                self.close()
            else:
                q.locked = True
                session.commit()
                self.sim_id = q.id
                self.send('Successfully established connection.')
        except sqlalchemy.orm.exc.NoResultFound:
            self.send(f'Error: no model found with id {model_id}.')
            self.close()
        except sqlalchemy.orm.exc.MultipleResultsFound:
            self.send(f'Error: multiple models found with id {model_id}.')
            self.close()
        except:
            session.rollback()
            self.close()
            raise
        finally:
            session.close()

    def on_message(self, message):
        if self.sim_id != None:
            try:
                self.receive(message)
            except tornado.websocket.WebSocketClosedError:
                self.receive('WebSocket closed by client.')
                pass

    def on_close(self):
        session = Session()
        try:
            q = session.query(Simulation) \
                       .filter_by(socket_id=self.socket_id) \
                       .with_for_update().one()
            if not q.locked:
                self.receive('Internal server error: sim is unsynchronized.')
            elif self.sim_id != None:
                q.locked = False
                session.commit()
                self.receive('Successfully terminated connection.')
        except sqlalchemy.orm.exc.NoResultFound:
            self.receive(f'Error: no model found with id {model_id}.')
        except sqlalchemy.orm.exc.MultipleResultsFound:
            self.receive(f'Error: multiple models found with id {model_id}.')
        except:
            session.rollback()
            raise
        finally:
            session.close()


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
