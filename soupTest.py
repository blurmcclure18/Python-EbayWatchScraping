from bs4 import BeautifulSoup
from pathlib import Path
import os

resultsCounter = 0
myResults = {}

currentDir = os.path.dirname(__file__)
SourceFiles = "SourceFiles"

try:
    os.mkdir(SourceFiles)
except:
    pass

SourceFilesDir = currentDir + '/' + SourceFiles

postNewSoup = open(SourceFilesDir + '/' + '(291) elgin.html')
#soup = BeautifulSoup(preNewSoup, "html.parser")
newSoup = BeautifulSoup(postNewSoup, 'html.parser')

def parse(soupName,soup):
    results = soup.find_all('div', {'class': 's-item__info clearfix'})

    print(f"\nWriting results to {soupName}.html: ")

    newSoup = soup.find("div", {'class': 'srp-merch__items clearfix'})

    numResults = len(results)
    print("\nNumber of Results: ")
    print(numResults)

    print("\nLooping Results: ")

    for item in results:
        try:
            product = {
                'title': item.find('h3', {'class': 's-item__title s-item__title--has-tags'}).text,
                'soldprice': float(item.find('span', {'class': 's-item__price'}).text.replace('$',"").replace(',','').strip()),
            }
            print(product)
        except:
            pass

print("\nTesting New Soup: ")
parse("NewSoup",newSoup)