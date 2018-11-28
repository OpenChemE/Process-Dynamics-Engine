from sqlalchemy import create_engine
from sqlalchemy import Boolean, Column, ForeignKey, Integer, PickleType, String
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Model(Base):

    __tablename__ = 'models'

    # TODO: serialize inputs and outputs as JSON strings
    id = Column(Integer, primary_key=True)
    name = Column(String)
    system = Column(PickleType)
    inputs = Column(PickleType)
    outputs = Column(PickleType)

    sims = relationship('Simulation', backref='models')

    def __repr__(self):
        return f"<Model(id={self.id}, name='{self.name}'>"


class Simulation(Base):

    __tablename__ = 'sims'

    id = Column(Integer, primary_key=True)
    model_id = Column(Integer, ForeignKey('models.id'))
    socket_id = Column(String(36), index=True)
    locked = Column(Boolean)
    data = Column(PickleType)

    def __repr__(self):
        return f"<Simulation(id={self.id}, " + \
                f'model_id={self.model_id}, socket_id={self.socket_id}>'


engine = create_engine('sqlite:///:memory:')
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
