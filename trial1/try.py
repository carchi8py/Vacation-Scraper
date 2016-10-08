import requests
from bs4 import BeautifulSoup

r = requests.get("http://pythonhow.com/example.html")
c = r.content
soup = BeautifulSoup(c, "html.parser")
all = soup.find_all("div", {"class":"cities"})
for each in all:
    cities = each.find_all("h2")
    for city in cities:
        print city.text
    