import os
import json
import threading
import shutil as sh
import pprint as pp
from time import sleep
import concurrent.futures
from random import randint
from bs4 import BeautifulSoup
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from PythonScripts.setup import watchgradeList
from selenium.webdriver.common.keys import Keys
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

def fool():
    sleep(randint(2,12))

def ebayBrowser(watchGrade,status):
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
    if status == "L":
        ebayListedUrl = f"https://www.ebay.com/sch/i.html?_from=R40&_nkw=elgin+grade+{watchGrade}+movement&_sacat=0&rt=nc&LH_BIN=1"
        browser.get(ebayListedUrl)
    else:
        ebayUrl = "https://www.ebay.com/"
        ebaySoldUrl = f"https://www.ebay.com/sch/i.html?_odkw=&_ipg=25&_sadis=200&_adv=1&_sop=12&LH_SALE_CURRENCY=0&LH_Sold=1&_osacat=0&_from=R40&_dmd=1&LH_Complete=1&_trksid=m570.l1313&_nkw=elgin+grade+{watchGrade}&_sacat=0"
        browser.get(ebayUrl)

    with open(f"{currentDir}/Settings/Cookies/cookies.json", 'r') as cookiesfile:
        cookies = json.load(cookiesfile)
    
    for cookie in cookies:
        browser.add_cookie(cookie)
    
    browser.refresh()

    if status == "S":
        fool()
        browser.get(ebaySoldUrl)
    else:
        pass
    
    return browser

def performActions(watchGrade, browser, status):
    # Automate the browser using selenium    
    # Change items per page
    browser.implicitly_wait(10)
    
    try:
        items_dropdown = browser.find_element(By.XPATH,
            "/html/body/div[5]/div[5]/div[2]/div[1]/div[2]/ul/div[3]/div[2]/div/span[2]/button/span"
        )
        items_dropdown.click()

        fool()

        items_200 = browser.find_element(By.XPATH,
            "/html/body/div[5]/div[5]/div[2]/div[1]/div[2]/ul/div[3]/div[2]/div/span[2]/span/ul/li[3]/a/span"
        )
        items_200.click()
    except:
        pass

    # Get the page source html
    browser.implicitly_wait(5)
    ebay_pagesource = browser.page_source

    # Close the browser
    browser.quit()

    # Parse html into Soup with BeautifulSoup
    soup = BeautifulSoup(ebay_pagesource, "html.parser")

    # Remove "Related Items" section that would give false info
    newSoup = soup

    # Write the Beautified Soup to html file for parsing
    with open(f"{currentDir}/TempFiles/{watchGrade}{status}.html","w") as writer:
        writer.write(str(soup))

def parseData(watchGrade, status):
    # Parse Data based on Sold or Listed Status
    global resultsCounter
    
    # Create lock for threading
    global lock
    lock = threading.Lock()    

    if status == "S":
        # Get the counter to create dictionary entries
        global resultsCounter

        # Import and rebeautify it
        soup = open(f"{currentDir}/TempFiles/{watchGrade}{status}.html","r")
        newSoup = BeautifulSoup(soup, "html.parser")
    
        # Get all Sold Listings Data
        results = newSoup.find_all("div", {"class": "s-item__info clearfix"})
    
        # With Threading iterate adding sold prices to list and average them
        with lock:
            # list to store sold prices
            gradeSoldPrices = []
    
            for item in results:
                try:
                    title = item.find(
                        "h3", {"class": "s-item__title s-item__title--has-tags"}
                    ).text
    
                    if (("elgin" or "Elgin" or "ELGIN") and watchGrade) in title:
                        soldprice = float(
                            item.find("span", {"class": "s-item__price"})
                            .text.replace("$", "")
                            .replace(",", "")
                            .strip()
                        )
                        gradeSoldPrices.append(soldprice)
                    else:
                        pass
                except:
                    pass
                
            averagePrice = round(sum(gradeSoldPrices) / len(gradeSoldPrices))
    
            # Add the watch grade and average price to dictionary
            watchResults[resultsCounter] = {
                "grade": watchGrade,
                "averagePrice": averagePrice,
            }
    
            # Increase counter for next iteration
            resultsCounter += 1
    else:
        # Get the counter to create dictionary entries

        global avgPrices
        global watchListed

        # Import and rebeautify it
        soup = open(f"{currentDir}/TempFiles/{watchGrade}{status}.html","r")
        newSoup = BeautifulSoup(soup, "html.parser")

        # Get all Listings Data
        results = newSoup.find_all('li',{'class': 's-item s-item__pl-on-bottom s-item--watch-at-corner'})

        # With Threading iterate adding prices to list and average them
        with lock:
            # Get WatchGrade Average Price
            for n in avgPrices:
                if avgPrices[n]['grade'] == watchGrade:
                    watchAvg = avgPrices[n]['averagePrice']
                else:
                    pass

            for item in results:
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

                    if (("elgin" or "Elgin" or "ELGIN") and watchGrade) in title:
                        if price < watchAvg:
                            product = {
                                'title': title,
                                'price': price,
                                'link': item.find('a', {'class' : 's-item__link'})['href'],
                                'image': image
                            }
                            print(f'\nParsed {product}')
                        else:
                            pass

                        # Add the watch grade and average price to dictionary
                        watchListed[resultsCounter] = {
                            "grade": watchGrade,
                            "watch": product,
                        }

                        # Increase counter for next iteration
                        resultsCounter += 1
                    else:
                        pass
                except:
                    pass

    if status == "L":
        # Parse Good Results
        counter = 0
        for entry in watchListed:
            if watchListed[entry]['grade'] == watchGrade:
                if watchGrade not in MasterDict:
                    MasterDict[watchGrade]= {counter: watchListed[entry]['watch']}
                    counter += 1
                else:
                    MasterDict[watchGrade][counter] = watchListed[entry]['watch']
                    counter += 1
            else:
                pass
    else:
        pass

def getHandles(watchGrade, browser, status):
    # Using threading perform these functions based on their status 
    performActions(watchGrade, browser, status)
    parseData(watchGrade,status)

def setupWorkers(grade_list, status):
    # create workers and list to perform threading
    workers = len(grade_list)
    browsers = []

    # Add open browsers to list to use
    while len(browsers) < workers:
        for grade in grade_list:
            browsers.append(ebayBrowser(grade, status))
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        executor.map(getHandles, grade_list, browsers, status)

# Create Main Function
def newMain(gradeList):
    global avgPrices

    #Run our Program
    createSourceDir()

    # Testing Sold Functions
    #getHandles('291',ebayBrowser('291',"S"),"S")

    #Get Sold Data
    setupWorkers(gradeList,"S")

    # Update Average Prices
    avgPrices = watchResults

    # Testing Listed Functions
    #getHandles('291',ebayBrowser('291',"L"),"L")

    # Get Listed Items Data
    setupWorkers(gradeList,"L")

    # Print Final Results
    print('\nPrinting Master Watch List: ')
    pp.pprint(MasterDict)

    # Remove our TempFiles directory to save space
    sh.rmtree(TempFilesDir, ignore_errors=True)

# Create a counter to increment results dictionary
resultsCounter = 0

# Results dictionary that will hold our watch grade with their average price
watchResults = {}
avgPrices = {}

# Results dictionary that will hold our watches
watchListed = {}
MasterDict = {}

# Call Main Function
newMain(watchgradeList)