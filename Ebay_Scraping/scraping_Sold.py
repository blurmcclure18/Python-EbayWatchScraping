import requests
from bs4 import BeautifulSoup
import pandas as pd
import pprint as pp

headers = {
    "User-Agent":
    "Edge/95.0.1020.40"
}

test_sold_url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1312.R1.TR11.TRC2.A0.H0.XIp.TRS1&_nkw=(291)+elgin&LH_Complete=1&LH_Sold=1&_oac=1"

def test_get_data(url):
    s = requests.session()
    r = s.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    with open(f"testing.html", 'w') as writer:
        writer.write(str(soup))
    return soup

def parse_sold(soups_dict):
    counter = 0
    print("\nSold Listing Results: ")
    results = soups_dict.find_all('div', {'class': 's-item__info clearfix'})
    print(len(results))
    return

my_soup_sold = test_get_data(test_sold_url)
parse_sold(my_soup_sold)