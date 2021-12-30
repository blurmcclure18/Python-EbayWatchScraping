# Author Alec McClure
import json
import os
import pprint
from ebaysdk.finding import Connection as finding
from ebaysdk.exception import ConnectionError

from ebayapi import ebayapi  # My API key
from ebayapi import ebayapiSand

# API_KEY = ebayapi
API_KEY = ebayapiSand
keywords = input("Enter Keywords: ")


class Ebay_21(object):
    def __init__(self, API_KEY):
        self.api_key = API_KEY

    def fetchListed(self, search):
        try:
            api = finding(
                appid=self.api_key,
                config_file=None,
                domain="api.sandbox.ebay.com",
            )
            response = api.execute("findItemsAdvanced", {"keywords": f"{search}"})
            counter = 1
            newInfo = {}
            for item in response.reply.searchResult.item:
                print(f"Condition: {item.condition.conditionDisplayName}")
                print(f"Buy it now available: {item.listingInfo.buyItNowAvailable}")
                if item.listingInfo.buyItNowAvailable == "true":
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
            response = api.execute("findCompletedItems", {"keywords": f"{search}"})
            counter = 1
            newInfo = {}
            # for item in response.reply.searchResult.item:
            # print(f"Condition: {item.condition.conditionDisplayName}")
            # print(f"Buy it now available: {item.listingInfo.buyItNowAvailable}")
            # if item.listingInfo.buyItNowAvailable == "true":
            # newInfo[counter] = {
            #    "itemTitle": {item.title},
            #    "itemPrice": {item.sellingStatus.currentPrice.value},
            #    "itemLink": {item.viewItemURL},
            #    "buyItNowAvailable": {item.listingInfo.buyItNowAvailable},
            # }
            # counter += 1
            return response.dict()
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
    ebay_Listed = e.fetchListed(keywords)
    pprint.pprint(ebay_Listed)

    # ebay_Sold = e.fetchSold(keywords)
    # pprint.pprint(ebay_Sold)

    json_Listed = json.dumps(ebay_Listed, indent=4)

    # json_object = json.dumps(ebay_Sold, indent=4)

    e.parse(json_Listed, "sold.json")
