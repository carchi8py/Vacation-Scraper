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

engine = create_engine('sqlite:///curise.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

def main():
    urls = create_urls()

    if 'linux' in sys.platform:
        # start xvfb in case no X is running. Make sure xvfb 
        # is installed, otherwise this won't work!
        dryscrape.start_xvfb()
    
    # set up a web scraping session
    sess = dryscrape.Session(base_url = 'https://www.google.com/')
    
    # we don't need images
    sess.set_attribute('auto_load_images', False)
    
    # visit homepage and search for a term
    sess.visit('/flights/?f=0#search;f=SFO;t=SEA;d=2017-06-01;r=2017-06-08')
    #not really used, but if it isn't past bad thing happen
    q = sess.at_xpath('//*[@f="SFO"]')
    
    c = sess.body()
    
    soup = BeautifulSoup(c, "html.parser")
    print soup.prettify()
    spans = soup.find_all('span', {'elm':'il'})
    print spans
    for each in spans:
        divs = each.find_all('div')
        print divs[2].text
        for div in divs:
            continue

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