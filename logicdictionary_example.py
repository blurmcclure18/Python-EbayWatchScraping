import random as rand
import string
import pprint as pp


testDict = {}

letters = string.ascii_lowercase

counter = 0
while counter < 20:
    testDict[counter] = {
        "listing": "".join(rand.choice(letters) for i in range(6)),
        "price": rand.randint(10, 30),
    }
    counter += 1

listNums = []

for n in testDict:
    listNums.append(testDict[n]["price"])

average = sum(listNums) / len(listNums)

print(f"The average price is : {average}")

deals = {}
deals_counter = 0
for n in testDict:
    if testDict[n]["price"] < average:
        deals[deals_counter] = testDict[n]
        deals_counter += 1
    else:
        pass

for n in testDict:
    pp.pprint(testDict[n])
