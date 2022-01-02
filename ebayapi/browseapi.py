#import browseapi
from browseapi.client import BrowseAPI
from ebayapi import ebayapi
from ebayapi import certid

app_id = ebayapi
cert_id = certid

api = BrowseAPI(app_id, cert_id)
responses = api.execute(
    'search', [{'q': '(303) elgin', 'limit': 10}, {'category_ids': 3937}])

print(responses[0].itemSummaries[0])
