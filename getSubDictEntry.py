from watchAvgPrices import avgPrices

print(avgPrices)



for n in avgPrices:
    if avgPrices[n]['grade'] == '303':
        print(avgPrices[n]['averagePrice']) # Change this to store it in a variable for use in testing.py for current listings on ebay
    else:
        pass

#print(avgPrices['grade': '303'])