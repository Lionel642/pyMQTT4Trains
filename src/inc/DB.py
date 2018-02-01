from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Host(Base):
    __tablename__ = 'host'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

class Controler(Base):
    __tablename__ = 'controler'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    device = Column(Integer, nullable=False)
    tty = Column(String(250), nullable=False)
    host_id = Column(Integer, ForeignKey('host.id'))

class Servo(Base):
    __tablename__ = 'servo'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    controler_id = Column(Integer, ForeignKey('controler.id'))
    address = Column(Integer, nullable=False)
    accel = Column(Integer, nullable=False)
    posThrown = Column(Integer, nullable=False)
    posClosed = Column(Integer, nullable=False)
