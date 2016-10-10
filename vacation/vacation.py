import requests
from datetime import datetime
from decimal import *
from re import sub
from bs4 import BeautifulSoup

#import our data file
import data.cruise as c

#import the database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Cruise

engine = create_engine('sqlite:///curise.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

import sys

def main():
    urls = create_urls()
    cruises = []
    for url in urls:
        cruises = get_cruises(url, cruises)
    for cruise in cruises:
        date_string = cruise['date']
        date_object = datetime.strptime(date_string, '%b %d, %Y')
        value = int(Decimal(sub(r'[^\d.]', '', cruise['price'])))
        new_cruise = Cruise(date = date_object.date(),
                            line = cruise['line'],
                            ship = cruise['ship'],
                            depart = cruise['depart'],
                            nights = int(cruise['nights']),
                            price = value)
        session.add(new_cruise)
        session.commit()
        

def create_urls():
    """
    Create curise URLS
    """
    urls = []
    for destination in c.destination:
        for departuredate in c.departuredate:
            for dport1 in c.dport1:
                urls.append(c.url_1 + 
                            destination + 
                            c.url_2 + 
                            departuredate + 
                            c.url_3 +
                            dport1 + 
                            c.url_4)
    return urls

def get_cruises(url, cruises):
    r = requests.get(url)
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    all  = soup.find("table", {"class": "cruise-search-table"})
    cruises_data = all.find("tbody").find_all("tr")
    for cruise in cruises_data:
        cruises.append(get_cruise_data(cruise))
    return cruises

def get_cruise_data(cruise):
    """
    col 1 = Data
    col 2 = Cruise line
    col 3 = Ship
    col 5 = departs
    col 6 = nights
    col 7 = price
    """
    cruise_data = {}
    data_col = cruise.find_all('td')
    cruise_data['date'] = data_col[0].text
    cruise_data['ur'] = data_col[0].find('a', href=True)['href']
    cruise_data['line'] = data_col[1].text
    cruise_data['ship'] = data_col[2].text
    cruise_data['depart'] = data_col[4].text
    cruise_data['nights'] = data_col[5].text
    cruise_data['price'] = data_col[6].text
    return cruise_data

if __name__ == '__main__':
    main()