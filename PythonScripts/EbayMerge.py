import os
import json
import requests
import threading
import shutil as sh
import pprint as pp
from time import sleep
import concurrent.futures
from random import randint
from bs4 import BeautifulSoup
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from PythonScripts.userSearch import keywordsList
from PythonScripts.userSearch import searchNameList
from PythonScripts.Settings.headless import headless
from selenium.webdriver.firefox.options import Options

# Get Current Working Directory to use in Functions
currentDir = os.path.dirname(__file__)
TempFilesDir = f"{currentDir}/TempFiles"

# Create funtions to use in program

def createSourceDir():
    # Create the folder to store temp html files
    try:
        os.mkdir(f"{currentDir}/TempFiles")
    except:
        pass

def testingBrowser():
    pass

def listedRequests(searchTerm, avgPrice):    
    # Set Ebay URL
    inUrlSearch = searchTerm.replace(' ', '+')
    ebayListedUrl = f"https://www.ebay.com/sch/i.html?_from=R40&_nkw={inUrlSearch}&_sacat=0&_udhi={avgPrice}&rt=nc&LH_BIN=1"
    listedPageSource = requests.get(ebayListedUrl).text

    return listedPageSource

def ebayBrowser(searchTerm):
   # Create and launch a FireFox Browser
    if os.name == "nt":
        geckoPath = (
            f"{currentDir}/SetupScripts/WindowsScript/WinGeckoWebDriver/geckodriver.exe"
        )
    else:
        pass

    if os.name == "posix":
        geckoPath = f"{currentDir}/SetupScripts/BashScript/LinuxGeckoWebDriver/geckodriver"
    else:
        pass

    # Store options to use in Firefox
    firefoxOptions = Options()

    # Start a headless browser (comment out the below line to view what the browser is doing )
    if headless == True:
        firefoxOptions.headless = True
    else:
        firefoxOptions.headless = False
    
    # Run the browser
    browser = wd.Firefox(executable_path=geckoPath, options=firefoxOptions)

    browser.implicitly_wait(10)
    
    # Set Ebay URL
    inUrlSearch = searchTerm.replace(' ', '+')
    ebayUrl = 'https://ebay.com'
    ebaySoldUrl = f"https://www.ebay.com/sch/i.html?_odkw=&_ipg=25&_sadis=200&_adv=1&_sop=12&LH_SALE_CURRENCY=0&LH_Sold=1&_osacat=0&_from=R40&_dmd=1&LH_Complete=1&_trksid=m570.l1313&_nkw={inUrlSearch}&_sacat=0"

    browser.get(ebayUrl)

    browser.implicitly_wait(5)
     
    with open(f"{currentDir}/Settings/Cookies/loginCookies.json", 'r') as cookiesfile:
        cookies = json.load(cookiesfile)
    
    for cookie in cookies:
        browser.add_cookie(cookie)
    
    browser.refresh()

    browser.get(ebaySoldUrl)

    browser.implicitly_wait(5)

    verifySource = browser.page_source
    
    print('\nRunning Captcha Check...')

    captchaDetected = False
    try:
        soup = BeautifulSoup(verifySource, "html.parser")
        verifyText = soup.find("div", {"id": "areaTitle"}).text
        
        if "verify" in verifyText:
            print('\nCaptcha Detected...')
            captchaDetected = True
        else:
            print('\nNo Captcha Detected...')
    except:
        pass
    
    if captchaDetected == True:
        input('\nPress Enter After Completing Captcha')
    else:
        pass
    
    #try:
    #    items_dropdown = browser.find_element(By.XPATH,
    #        "/html/body/div[5]/div[5]/div[2]/div[1]/div[2]/ul/div[3]/div[2]/div/span[2]/button/span"
    #    )
    #    items_dropdown.click()

    #    sleep(randint(2,5))
    #    
    #    browser.implicitly_wait(5)

    #    items_200 = browser.find_element(By.XPATH,
    #        "/html/body/div[5]/div[5]/div[2]/div[1]/div[2]/ul/div[3]/div[2]/div/span[2]/span/ul/li[3]/a/span"
    #    )
    #    items_200.click()
    #except:
    #    pass

    ebaySold = browser.page_source

    # Parse html into Soup with BeautifulSoup
    soldSoup = BeautifulSoup(ebaySold, "html.parser")

    # Write the Beautified Soup to html file for parsing
    #with open(f"{currentDir}/TempFiles/{searchTerm}Sold.html","w") as writer:
    #    writer.write(str(soldSoup))
    
    browser.quit()

    return soldSoup

def parseData(searchTerm,searchName):

    soldSoup = ebayBrowser(searchTerm)

    # Parse Data based on Sold or Listed Status
    print('\nParsing Data...')
    
    # Create lock for threading
    lock = threading.Lock()

    with lock:
        # Import and rebeautify it
        print("\nImporting Sold Data...")
        #soldSoup = open(f"{currentDir}/TempFiles/{searchTerm}Sold.html","r")
        newSoldSoup = soldSoup#BeautifulSoup(soldSoup, "html.parser")

        # Get all Sold Listings Data
        soldResults = newSoldSoup.find_all("div", {"class": "s-item__info clearfix"})
        
        # list to store sold prices
        itemSoldPrices = []

        print('\nStarting Average Price Loop...')

        # Results dictionary that will hold our item with it's average price
        searchResults = {}
        soldCounter = 0

        for item in soldResults:
            try:
                title = item.find(
                    "h3", {"class": "s-item__title s-item__title--has-tags"}
                ).text
                
                lowerSoldTitle = title.lower().split(' ')

                lowerSoldSearch = searchTerm.lower().split(' ')

                lowerSoldSearchResults = []

                for word in lowerSoldTitle:
                    for term in lowerSoldSearch:
                        if term == word:
                            if word not in lowerSoldSearchResults:
                                lowerSoldSearchResults.append(word)
                        else:
                            pass

                if len(lowerSoldSearchResults) == len(lowerSoldSearch):
                    soldprice = float(
                        item.find("span", {"class": "s-item__price"})
                       .text.replace("$", "")
                       .replace(",", "")
                       .strip()
                    )
                    itemSoldPrices.append(soldprice)
                else:
                    pass
            except:
                pass
        
        if len(itemSoldPrices) > 0:
            averagePrice = round(sum(itemSoldPrices) / len(itemSoldPrices))
            print(f'\nAverage Price: {averagePrice}')
        else:
            print('\nNo Sold Items Found...')
            return

        # Add the item and average price to dictionary
        searchResults[soldCounter] = {
            "item": searchName,
            "averagePrice": averagePrice,
        }

        # Increase counter for next iteration
        soldCounter += 1

        # Results dictionary that will hold our Listed Items
        searchListed = {}

        # Get the Item Average Price
        print('\nFinding Average Price...')
        for n in searchResults:
            if searchResults[n]['item'] == searchName:
                itemAvg = searchResults[n]['averagePrice']
            else:
                print(f"\nCannot Find Average Price for search {searchResults[n]['item']}")
    
        print('\nGetting Current Listings...')
        # Import and rebeautify it
        listedSoup = listedRequests(searchTerm, itemAvg)
        newListedSoup = BeautifulSoup(listedSoup, "html.parser")
        
        # Get all Listings Data
        listedResults = newListedSoup.find_all('li',{'class': 's-item s-item__pl-on-bottom s-item--watch-at-corner'})
        
        listedCounter = 0

        for item in listedResults:
            try:
                image = item.find('img', {'class' : 's-item__image-img'})['src']
                title = item.find(
                    "h3", {"class": "s-item__title"}
                ).text
                price = float(
                            item.find("span", {"class": "s-item__price"})
                            .text.replace("$", "")
                            .replace(",", "")
                            .strip()
                        )
                
                lowerListedTitle = title.lower().split(' ')
                lowerListedSearch = searchTerm.lower().split(' ')

                lowerListedSearchResults = []

                for word in lowerListedTitle:
                    for term in lowerListedSearch:
                        if term == word:
                            if word not in lowerListedSearchResults:
                                lowerListedSearchResults.append(word)
                        else:
                            pass

                if len(lowerListedSearchResults) == len(lowerListedSearch):
                    if price < itemAvg:
                        product = {
                            'title': title,
                            'price': price,
                            'link': item.find('a', {'class' : 's-item__link'})['href'],
                            'image': image
                        }
                    else:
                        pass

                    # Add the watch grade and average price to dictionary
                    searchListed[listedCounter] = {
                        "search": searchName,
                        "item": product,
                    }

                    # Increase counter for next iteration
                    listedCounter += 1
                else:
                    pass
            except:
                pass
        
        # Parse Good Results
        counter = 0
        for entry in searchListed:
            if searchListed[entry]['search'] == searchName:
                if searchName not in MasterDict:
                    MasterDict[searchName]= {counter: searchListed[entry]['item']}
                    counter += 1
                else:
                    MasterDict[searchName][counter] = searchListed[entry]['item']
                    counter += 1
            else:
                pass
    print('\nData Parsed...')
    return

def getHandles(searchTerm, searchName):
    # Using threading perform these functions
    print('\nGetting Handles...')
    #ebayBrowser(searchTerm)
    parseData(searchTerm,searchName)

def setupWorkers(searchTermList,nameList):
    # create workers and list to perform threading
    print('\nStarting Workers...')
    workers = len(searchTermList)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        executor.map(getHandles, searchTermList, nameList)

# Create Main Function
def newMain(searchTermList, nameList):
    #Run our Program
    createSourceDir()

    # Testing Functions
    #getHandles('elgin grade 95', 'Elgin 95')
    # Perform a Captcha Check before launching Threaded Browsers
    #captchaCheck(testBrowser(searchTermList[0]))

    #Get Data
    setupWorkers(searchTermList, nameList)

    # Remove our TempFiles directory to save space
    sh.rmtree(TempFilesDir, ignore_errors=True)

MasterDict = {}

# Call Main Function
newMain(keywordsList, searchNameList)

if len(MasterDict) > 0:
    # Print Final Results
    print('\n\nPrinting Master List: ')
    pp.pprint(MasterDict)
else:
    print("\nCouldn't find any items that matched your search critera try refining your search.")

with open(f'{currentDir}/MasterDict.py','w', encoding='utf-8') as writer:
    writer.write(f'MasterDict = {MasterDict}')