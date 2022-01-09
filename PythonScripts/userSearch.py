# Add Keywords for Ebay Search in other programs
def getUserSearch():
    userDoneFinal = ['',]
    whileCounter = 0
    print(userDoneFinal[whileCounter])
    while userDoneFinal[whileCounter] != 'no':
        searchNameList.append(input('\nCreate a Name for your Search:\n'))
        keywordsList.append(input('\nPlease enter your search term:\n'))
        userDoneFinal.append(input('\nWould you like to add another search?:\n').lower())
        whileCounter += 1


searchNameList = []
keywordsList = []

getUserSearch()