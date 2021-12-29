#Author Alec McClure

import os
from ebaysdk.finding import Connection as finding
from ebaysdk.exception import ConnectionError

from dotenv import load_dotenv
load_dotenv()
API_KEY=os.getenv('api_key')

class Ebay_21(object):
    def __init__(self, API_KEY):
        self.api_key = API_KEY

    def fetch(self):
        try:
            api = finding(appid=self.api_key, config_file=None)
            response = api.execute('findItemsAdvanced', {'keywords': 'Python'})
            print(response.dict())
        except ConnectionError as e:
            print(e)
            print(e.response.dict())

    def parse(self):
        pass

# main driver

if __name__ == '__main__':
        e = Ebay_21(API_KEY)
        e.fetch()
        e.parse()
