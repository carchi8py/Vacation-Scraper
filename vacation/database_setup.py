import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Cruise(Base):
    __tablename__ = 'cruise'
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable = False)
    line = Column(String(250), nullable = False)
    ship = Column(String(250))
    depart = Column(String(250))
    nights = Column(Integer)
    price = Column(Integer)
    
class Flight(Base):
    __tablename__ = 'cruise'
    id = Column(Integer, primary_key=True)
    price = Column(Integer)
    start = Column(String(250))
    cruise_id = Column(Integer, ForeignKey('cruise.id'))
    cruise = relationship(Cruise)

engine = create_engine('sqlite:///curise.db')
Base.metadata.create_all(engine)
