import dryscrape
import sys
import datetime
from bs4 import BeautifulSoup

#import our data file
import data.plane as p

#import the database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Cruise
import time
from random import randint

engine = create_engine('sqlite:///curise.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

def main():
    urls = create_urls()
    urls = list(set(urls))
    
    for url in urls:
        print url
        flight = get_flights(url)
        curises = session.query(Cruise).filter_by(date=flight[3], depart=p.a_code[flight[2]])
        for cruise in curises:
            if flight[1] == 'SFO':
                if cruise.cal == 0 or cruise.cal < 100000000:
                    cruise.cal = flight[0]
            else:
                if cruise.can == 0 or cruise.can < 100000000:
                    cruise.can = flight[0]
            session.add(cruise)
            session.commit()
        sleep_time = randint(10,60)
        print 'sleeping for ' + str(sleep_time)
        time.sleep(sleep_time)

def get_flights(url):
    if 'linux' in sys.platform:
        # start xvfb in case no X is running. Make sure xvfb 
        # is installed, otherwise this won't work!
        dryscrape.start_xvfb()
    
    # set up a web scraping session
    sess = dryscrape.Session(base_url = 'https://www.google.com/')
    # we don't need images
    sess.set_attribute('auto_load_images', False)
    
    # visit homepage and search for a term
    sess.visit(url)
    #not really used, but if it isn't past bad thing happen
    q = sess.at_xpath('//*[@f="SFO"]')
    
    c = sess.body()
    
    soup = BeautifulSoup(c, "html.parser")
    spans = soup.find_all('span', {'elm':'il'})
    lowest_price = 100000000
    for each in spans:
        divs = each.find_all('div')
        price = divs[2].text
        if len(price) > 7:
            price = price[0:4]
        if len(price) < 2:
            price = 0
        price = int(price[1:])
        if price < lowest_price:
            lowest_price = price
    return format_data(lowest_price, url)

def format_data(lowest_price, url):
    start = url.split(p.url_1)[1].split(p.url_2)[0]
    end = url.split(p.url_2)[1].split(p.url_3)[0]
    depart = url.split(p.url_3)[1].split(p.url_4)[0]
    return [lowest_price, start, end, depart]

def create_urls():
    """
    Generate all the google flight urls we need for all the dates we care about
    """
    urls = []
    #first we need to get all our cruise to find out the date we need to look 
    #up flight for 
    curises = session.query(Cruise).order_by(Cruise.date)
    for cruise in curises:
        start_date = cruise.date
        end_date = cruise.date + datetime.timedelta(cruise.nights)
        airport_code = p.b_code[cruise.depart]
        for start in p.f:
            if airport_code == start:
                continue
            urls.append(p.url_1 + start + p.url_2 + airport_code + p.url_3 + \
                        str(start_date) + p.url_4 + str(end_date))

    return urls


if __name__ == '__main__':
    main()