# Author Alec McClure

import json
import os
import pprint
import smtplib
from sendDeals import sendEmail
from ebaysdk.finding import Connection as finding
from ebaysdk.exception import ConnectionError
from ebayapi import ebayapi  # My API key

API_KEY = ebayapi

keywords = input("Enter Keywords: ")


class Ebay_21(object):
    def __init__(self, API_KEY):
        self.api_key = API_KEY

    def fetchListed(self, search, averagePrice):
        try:
            api = finding(
                appid=self.api_key,
                config_file=None,
            )
            response = api.execute(
                "findItemsAdvanced",
                {
                    "keywords": f"{search}",
                    "categoryId": "3937",
                    "itemFilter": {"name": "MaxPrice", "value": f"{averagePrice}"},
                    "paginationInput": {"entriesPerPage": "10", "pageNumber": "1"},
                },
            )
            counter = 1
            newInfo = {}
            for item in response.reply.searchResult.item:
                if item.sellingStatus.currentPrice.value < averagePrice:
                    newInfo[counter] = {
                        "itemTitle": {item.title},
                        "itemPrice": {item.sellingStatus.currentPrice.value},
                        "itemLink": {item.viewItemURL},
                        "buyItNowAvailable": {item.listingInfo.buyItNowAvailable},
                    }
                counter += 1
            return newInfo
        except ConnectionError as e:
            print(e)
            print(e.response.dict())

    def fetchSold(self, search):
        try:
            api = finding(appid=self.api_key, config_file=None)
            response = api.execute(
                "findCompletedItems",
                {
                    "keywords": f"{search}",
                    "categoryId": "3937",
                    "paginationInput": {"entriesPerPage": "10", "pageNumber": "1"},
                },
            )
            counter = 1
            soldInfo = {}
            for item in response.reply.searchResult.item:
                soldInfo[counter] = {
                    "itemTitle": {item.title},
                    "itemPrice": {item.sellingStatus.currentPrice.value},
                    "itemLink": {item.viewItemURL},
                    "buyItNowAvailable": {item.listingInfo.buyItNowAvailable},
                }
                counter += 1

            priceList = []

            for n in soldInfo:
                priceList.append(float(soldInfo[n]["itemPrice"]))

            average = sum(priceList) / len(priceList)

            return average

        except ConnectionError as e:
            print(e)
            print(e.response.dict())

    def parse(self, some_data, outputFile):
        file = open(f"{outputFile}", "w")
        file.write(some_data)
        file.close
        return print(f"Check {outputFile} for output")


# main driver

if __name__ == "__main__":
    e = Ebay_21(API_KEY)

    deals = e.fetchListed(keywords, e.fetchSold(keywords))

    pprint.pprint(deals)

    # sendEmail()
