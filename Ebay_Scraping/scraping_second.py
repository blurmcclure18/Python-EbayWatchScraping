import requests
from bs4 import BeautifulSoup
import pandas as pd
import pprint as pp

# List of item names to search on eBay
name_list = ["(303) elgin", "(291) elgin"]
sold_Keywords = []

for n in name_list:
    sold_Keywords.append(n.split("(")[1].split(")")[0])

# Returns a list of urls that search eBay for an item
def make_urls(names):
    # eBay url that can be modified to search for a specific item on eBay
    url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1312.R1.TR11.TRC2.A0.H0.XIp.TRS1&_nkw="

    # List of urls created
    urls = []
    for name in names:
        # Adds the name of item being searched to the end of the eBay url and appends it to the urls list
        # In order for it to work the spaces need to be replaced with a +

        urls.append(url + name.replace(" ", "+"))  # Uncomment to see Current Listings

    # prints urls for testing
    # print("Current Urls:\n " + str(urls))

    # Returns the list of completed urls
    return urls


def make_urls_sold(names):
    # eBay url that can be modified to search for a specific item on eBay
    sold_url = "https://www.ebay.com/sch/i.html?_from=R40&_nkw={}&_sacat=3937&mkcid=1&mkrid=711-53200-19255-0&siteid=0&campid=5337798087&customid=&toolid=10001&mkevt=1&rt=nc&LH_Sold=1&LH_Complete=1"
    # List of urls created
    urls = []
    sold_urls = []
    for name in names:
        # Adds the name of item being searched to the end of the eBay url and appends it to the urls list
        # In order for it to work the spaces need to be replaced with a +

        urls.append(
            sold_url.format(name.replace(" ", "+"))
        )  # Uncomment to see Sold Listings

    # prints urls for testing
    print("Sold Urls:\n " + str(urls))

    # Returns the list of completed urls
    return urls


def get_data(urls):

    soup_output = {}
    counter = 0
    for url in urls:
        r = requests.get(url)
        soup_output[counter] = {"html": BeautifulSoup(r.text, "html.parser")}
        counter += 1
    return soup_output


def parse_current(soups_dict):
    counter = 0
    print("\nCurrent Listing Results: ")
    for n in soups_dict:
        html_soup = soups_dict[counter]["html"]
        results = html_soup.find_all("div", {"class": "s-item__info clearfix"})
        print(len(results))
        counter += 1
    return


my_soup_current = get_data(make_urls(name_list))
parse_current(my_soup_current)
