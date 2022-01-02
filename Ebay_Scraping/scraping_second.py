import requests
from bs4 import BeautifulSoup
import pandas as pd
import pprint as pp
import time

headers = {"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Edge/95.0.1020.40"}

#headers = {"User-Agent":"Edge/95.0.1020.40"}

# List of item names to search on eBay
#keywords = input("Enter Keywords: ")
name_list = ["(303) elgin", "(291) elgin"]

#test_sold_url = "http://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1312.R1.TR11.TRC2.A0.H0.XIp.TRS1&_nkw=(291)+elgin&LH_Complete=1&LH_Sold=1&_oac=1"

# Returns a list of urls that search eBay for an item
def make_urls_current(names):
    # eBay url that can be modified to search for a specific item on eBay
    url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1312.R1.TR11.TRC2.A0.H0.XIp.TRS1&_nkw="

    # List of urls created
    urls = []
    sold_urls = []
    for name in names:
        # Adds the name of item being searched to the end of the eBay url and appends it to the urls list
        # In order for it to work the spaces need to be replaced with a +
        
        urls.append(url + name.replace(" ", "+")) # Uncomment to see Current Listings

    # prints urls for testing
    # print("Current Urls:\n " + str(urls))


    # Returns the list of completed urls
    return urls

def make_urls_sold(names):
    # eBay url that can be modified to search for a specific item on eBay    
    sold_url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1312.R1.TR11.TRC2.A0.H0.XIp.TRS1&_nkw={}&LH_Complete=1&LH_Sold=1&_oac=1"
    # List of urls created
    urls = []
    sold_urls = []
    for name in names:
        # Adds the name of item being searched to the end of the eBay url and appends it to the urls list
        # In order for it to work the spaces need to be replaced with a +
    
        urls.append(sold_url.format(name.replace(" ", "+"))) # Uncomment to see Sold Listings

    # prints urls for testing
    # print("Sold Urls:\n " + str(urls))

    # Returns the list of completed urls
    return urls

def test_get_data(url):
    s = requests.session()
    r = s.get(url, headers=headers, verify=False)
    soup = BeautifulSoup(r.text, 'html.parser')
    with open(f"testing.html", 'w') as writer:
        writer.write(str(soup))
    
    return soup

def get_data(urls):
    
    soup_output = {}
    counter = 0
    for url in urls:
        s = requests.session()
        r = s.get(url, headers=headers)
        soup_output[counter]= {'html': BeautifulSoup(r.text, 'html.parser')}
        counter += 1
        

    return soup_output

def parse_current(soups_dict):
    counter = 0
    print("\nCurrent Listing Results: ")
    for n in soups_dict:
        html_soup = soups_dict[counter]['html']
        results = html_soup.find_all('div', {'class': 's-item__info clearfix'})
        print(len(results))
        counter += 1
    return

def parse_sold(soups_dict):
    counter = 0
    print("\nSold Listing Results: ")
    for n in soups_dict:
        html_soup = soups_dict[counter]['html']
        results = soups_dict.find_all('div', {'class': 's-item__info clearfix'})
        print(len(results))
        counter += 1
    return

my_soup_current = get_data(make_urls_current(name_list))
parse_current(my_soup_current)

my_soup_sold = get_data(make_urls_sold(name_list))
parse_current(my_soup_sold)

#my_soup_sold = test_get_data(test_sold_url)
#parse_sold(my_soup_sold)
