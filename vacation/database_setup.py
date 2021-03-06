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
    cal = Column(Integer, default = 0)
    can = Column(Integer, default = 0)
    url = Column(String(250))
    day1 = Column(String(250))
    day2 = Column(String(250))
    day3 = Column(String(250))
    day4 = Column(String(250))
    day5 = Column(String(250))
    day6 = Column(String(250))
    day7 = Column(String(250))
    day8 = Column(String(250))
    day9 = Column(String(250))
    day10 = Column(String(250))
    day11 = Column(String(250))
    day12 = Column(String(250))
    day13 = Column(String(250))
    day14 = Column(String(250))
    day15 = Column(String(250))

engine = create_engine('sqlite:///curise.db')
Base.metadata.create_all(engine)
