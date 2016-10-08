import requests
from bs4 import BeautifulSoup

#import our data file
import data.cruise as c

import sys


def main():
    urls = create_urls()
    for url in urls:
        cruises = get_cruises(url)
        

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

def get_cruises(url):
    r = requests.get(url)
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    all  = soup.find("table", {"class": "cruise-search-table"})
    cruises = all.find("tbody").find_all("tr")
    for cruise in cruises:
        get_cruise_data(cruise)

def get_cruise_data(cruise):
    return cruise

if __name__ == '__main__':
    main()