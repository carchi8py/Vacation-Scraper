import requests
from datetime import datetime
from decimal import *
from re import sub
from bs4 import BeautifulSoup

#import our data file
import data.cruise as c
import time

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
        #Now that we have our cruise url we want to open them and see the ports
        details = get_cruise_details(c.url_details + cruise['url'])
        
        new_cruise = Cruise(date = date_object.date(),
                            line = cruise['line'],
                            url = c.url_details + cruise['url'],
                            ship = cruise['ship'],
                            depart = cruise['depart'],
                            nights = int(cruise['nights']),
                            price = value,
                            day1 = details[1],
                            day2 = details[2],
                            day3 = details[3],
                            day4 = details[4],
                            day5 = details[5],
                            day6 = details[6],
                            day7 = details[7],
                            day8 = details[8],
                            day9 = details[9],
                            day10 = details[10],
                            day11 = details[11],
                            day12 = details[12],
                            day13 = details[13],
                            day14 = details[14],
                            day15 = details[15])
        session.add(new_cruise)
        session.commit()
        print 'Curise added'
        time.sleep(10)

def get_cruise_details(url):
    details = {}
    r = requests.get(url)
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    all  = soup.findAll("table", {"class": "cruise-itinerary-table"})
    days = all[1].find("tbody").find_all("tr")
    day_count = 1
    for day in days:
        data_col = day.find_all('td')
        location = data_col[1].text.split(':')[1]
        details[day_count] = location
        day_count += 1
    while day_count < 16:
        details[day_count] = 'X'
        day_count += 1
    return details
     

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
    cruise_data['url'] = data_col[0].find('a', href=True)['href']
    cruise_data['line'] = data_col[1].text
    cruise_data['ship'] = data_col[2].text
    cruise_data['depart'] = data_col[4].text
    cruise_data['nights'] = data_col[5].text
    cruise_data['price'] = data_col[6].text
    return cruise_data

if __name__ == '__main__':
    main()