import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Cruise(Base):
    __tablename__ = 'cruise'
    date = Column(Date, nullable = False, primary_key=True)
    line = Column(String(250), nullable = False, primary_key=True)
    ship = Column(String(250))
    depart = Column(String(250))
    nights = Column(Integer)
    price = Column(Numeric)

engine = create_engine('sqlite:///curise.db')
Base.metadata.create_all(engine)