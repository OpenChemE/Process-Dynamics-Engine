import json, os, pickle, uuid
import tornado.gen, tornado.ioloop, tornado.web, tornado.websocket
import sqlalchemy.orm.exc

from models import Model, Session, Simulation
import wrapper


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        paragraphs = [
            'Process Dynamics Engine API Reference:',
            'GET /models/all: list all models',
            'POST /models/{model_id}: create a new simulation',
            'GET /sims/all: list all active simulations',
            'GET /sims/{sim_id}: get simulation status',
            'GET /sims/{sim_id}/{tag_id}: get tag status',
        ]
        self.write('<p>' + '</p><p>'.join(paragraphs) + '</p>')


class ModelListHandler(tornado.web.RequestHandler):

    def get(self):
        pass


class ModelCreateHandler(tornado.web.RequestHandler):

    def send(self, data):
        text = json.dumps(data)
        print(f'{data["status"]}: {data["message"]}')
        print(f'    {text}')
        self.write(text)

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with')
        self.set_header('Access-Control-Allow-Methods', 'POST')

    def post(self, model_id):
        model_id = int(model_id)
        session = Session()
        try:
            # Get the pickled model from the database
            model_row = session.query(Model) \
                               .filter_by(id=model_id) \
                               .with_for_update().one()

            # Generate a unique socket_id
            socket_id = str(uuid.uuid4())

            # Create a new row in the database
            sim_row = Simulation(
                model_id=model_id,
                socket_id=socket_id,
                locked=False,
            )

            # Get the id of the row in the database
            session.add(sim_row)
            session.flush()
            sim_id = sim_row.id

            # Create a new simulation object in Python
            sim_obj = wrapper.create(
                model_id,
                sim_id,
                model_row.name,
                model_row.system,
                model_row.inputs,
                model_row.outputs,
            )

            # Pickle the simulation object into the database
            sim_row.data = pickle.dumps(sim_obj)
            session.commit()

            self.send({
                'status': 'success',
                'message': 'created new simulation',
                'sim_id': sim_id,
                'model_id': model_id,
                'socket_id': socket_id,
            })
        except sqlalchemy.orm.exc.NoResultFound:
            self.set_status(404)
            self.send({
                'status': 'error',
                'message': 'no model found',
            })
            session.rollback()
        except sqlalchemy.orm.exc.MultipleResultsFound:
            self.set_status(500)
            self.send({
                'status': 'error',
                'message': 'multiple models found',
            })
            session.rollback()
        except Exception as e:
            self.set_status(500)
            self.send({
                'status': 'error',
                'message': str(e),
            })
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

    def send(self, data):
        text = json.dumps(data)
        if self.sim_id == None:
            print(f'to socket {self.socket_id}, '
                    + f'{data["status"]}: {data["message"]}')
            print(f'    {text}')
        else:
            print(f'to sim {self.sim_id}, {data["status"]}: {data["message"]}')
            print(f'    {text}')
        self.write_message(text)

    def receive(self, text):
        data = json.loads(text)
        if self.sim_id == None:
            print(f'from socket {self.socket_id}, '
                    + f'{data["status"]}: {data["message"]}')
            print(f'    {text}')
        else:
            print(f'from sim {self.sim_id}, {data["status"]}: {data["message"]}')
            print(f'    {text}')
        return data

    def check_origin(self, origin):
        # Allow access from local development server.
        if origin == 'file://':
            return True
        return False

    def open(self, socket_id):
        self.sim_id = None
        self.sim_obj = None
        self.socket_id = socket_id

        session = Session()
        try:
            # Get the pickled simulation from the database
            sim_row = session.query(Simulation) \
                             .filter_by(socket_id=self.socket_id) \
                             .with_for_update().one()

            # Check that the simulation is not locked
            if sim_row.locked:
                self.send({
                    'status': 'error',
                    'message': f'simulation {sim_row.id} is locked',
                })
                self.close()

            # Get the simulation object and lock the row in the database
            else:
                self.sim_id = sim_row.id
                self.sim_obj = pickle.loads(sim_row.data)
                sim_row.locked = True
                session.commit()

                if wrapper.is_active(self.sim_obj):
                    self.send({
                        'status': 'active',
                        'message': f'simulation {self.sim_id} is active',
                    })
                else:
                    self.send({
                        'status': 'inactive',
                        'message': f'simulation {self.sim_id} is inactive',
                    })

        except sqlalchemy.orm.exc.NoResultFound:
            self.send({
                'status': 'error',
                'message': f'no sim found for {self.socket_id}',
            })
            session.rollback()
            self.close()
        except sqlalchemy.orm.exc.MultipleResultsFound:
            self.send({
                'status': 'error',
                'message': 'multiple sims found for {self.socket_id}',
            })
            session.rollback()
            self.close()
        except Exception as e:
            self.send({
                'status': 'error',
                'message': str(e),
            })
            session.rollback()
            self.close()
        finally:
            session.close()

    def on_message(self, message):
        try:
            if self.sim_id != None:
                data = self.receive(message)
                if data['status'] == 'activate':
                    wrapper.activate(self.sim_obj)
                    self.send({
                        'status': 'active',
                        'message': f'activated simulation {self.sim_id}',
                    })
                else:
                    self.send({
                        'status': 'active',
                        'message': 'step',
                        'outputs': wrapper.step(self.sim_obj, data['inputs']),
                    })
        except tornado.websocket.WebSocketClosedError:
            self.receive(json.dumps({
                'status': 'backend',
                'message': 'websocket closed by client',
            }))
        except Exception as e:
            self.receive({
                'status': 'error',
                'message': str(e),
            })

    def on_close(self):
        session = Session()
        try:
            # Get the pickled simulation from the database
            sim_row = session.query(Simulation) \
                             .filter_by(socket_id=self.socket_id) \
                             .with_for_update().one()

            # Check that the row in the database is locked
            if not sim_row.locked:
                self.receive(json.dumps({
                    'status': 'error',
                    'message': 'internal server error, sim unsynchronized',
                }))

            # Unlock the row in the database
            elif self.sim_id != None:
                sim_row.locked = False
                sim_row.data = pickle.dumps(self.sim_obj)
                session.commit()
                self.receive(json.dumps({
                    'status': 'backend',
                    'message': 'successfully terminated connection',
                }))

            # Do nothing if self.sim_id is None
            else:
                self.receive(json.dumps({
                    'status': 'backend',
                    'message': 'successfully terminated connection',
                }))
        except sqlalchemy.orm.exc.NoResultFound:
            self.receive(json.dumps({
                'status': 'error',
                'message': f'no sim found for {self.socket_id}',
            }))
        except sqlalchemy.orm.exc.MultipleResultsFound:
            self.receive(json.dumps({
                'status': 'error',
                'message': 'multiple sims found for {self.socket_id}',
            }))
        except Exception as e:
            self.receive(json.dumps({
                'status': 'error',
                'message': str(e),
            }))
            session.rollback()
        finally:
            self.sim_id = None
            self.sim_obj = None
            session.close()


def make_app():
    # TODO: this is temporary code to initialize the available models
    session = Session()
    try:
        f = open('models/wood_berry.pkl', 'rb')
        pickled_model = pickle.load(f)
        session.add(Model(
            name='Wood-Berry Distillation',
            system=pickled_model.system,
            inputs=pickled_model.inputs,
            outputs=pickled_model.outputs,
        ))
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
        (r'/([0-9a-f\-]+)', WebSocketHandler),
    ])


if __name__ == '__main__':
    app = make_app()
    app.listen(int(os.environ.get('PORT', 8888)))
    tornado.ioloop.IOLoop.current().start()
