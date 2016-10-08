import dryscrape
import sys
from bs4 import BeautifulSoup

def main():

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



if __name__ == '__main__':
    main()