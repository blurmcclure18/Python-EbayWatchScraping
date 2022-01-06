import os
import json
import threading
import shutil as sh
import pprint as pp
from time import sleep
from pathlib import Path
import concurrent.futures
from random import randint
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.webdriver import WebDriver
from PythonScripts.setup import watchgradeList
from PythonScripts.watchAvgPrices import avgPrices
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

# Get Current Working Directory to use in Functions
currentDir = os.path.dirname(__file__)
TempFilesDir = f"{currentDir}/TempFiles"

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

# Create funtions to use in program

def createSourceDir():
    # Create the folder to store temp html files
    try:
        os.mkdir(f"{currentDir}/TempFiles")
    except:
        pass

def fool():
    sleep(randint(2,12))

def headlessBrowser(watchGrade):
    # Create and launch a FireFox Browser

    # Ebay Listings URL
    ebayUrl = f"https://www.ebay.com/sch/i.html?_from=R40&_nkw=elgin+grade+{watchGrade}+movement&_sacat=0&rt=nc&LH_BIN=1"

    # Store options to use in Firefox
    firefoxOptions = Options()

    # Start a headless browser (comment out the below line to view what the browser is doing )
    firefoxOptions.headless = True

    # Run the browser
    browser = wd.Firefox(executable_path=geckoPath, options=firefoxOptions)

    browser.implicitly_wait(10)

    browser.get(ebayUrl)

    with open(f"{currentDir}/Cookies/cookies.json", 'r') as cookiesfile:
        cookies = json.load(cookiesfile)
    
    for cookie in cookies:
        browser.add_cookie(cookie)
    
    browser.refresh()

    return browser

def perform_actions(watchGrade, browser):
    # Automate the browser using selenium

    # change items per page
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
    soup.find("div", {"class": "srp-merch__items clearfix"}).decompose()

    # Write the Beautified Soup to html file for parsing
    with open(f"{currentDir}/TempFiles/{watchGrade}.html","w") as writer:
        writer.write(str(newSoup))


def parseListed(watchGrade):
    # Parsing html to get prices

    # Create lock for threading
    global lock
    lock = threading.Lock()

    # Get the counter to create dictionary entries
    global resultsCounter

    # Import and rebeautify it
    soup = open(f"{currentDir}/TempFiles/{watchGrade}.html","r")
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
                
                buyItNow = item.find('span', {'class': 's-item__purchase-options-with-icon'}).text

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

def parseGoodResults(watchGrade):
    global lock

    with lock:
        counter = 0
        for entry in watchListed:
            if watchListed[entry]['grade'] == watchGrade:
                if watchGrade not in MasterDict:
                    MasterDict[watchGrade]= {counter: watchListed[entry]['watch']}
                    counter += 1
                else:
                    MasterDict[watchGrade][counter] = watchListed[entry]['watch']
                    counter += 1

def get_handles(watchGrade, browser):
    # Using threading perform these funtions
    perform_actions(watchGrade, browser)

    parseListed(watchGrade)

    parseGoodResults(watchGrade)


def setup_workers(grade_list):
    # create workers and list to perform threading
    workers = len(grade_list)
    browsers = []

    # Add open browsers to list to use
    while len(browsers) < workers:
        for grade in grade_list:
            browsers.append(headlessBrowser(grade))

    # Using ThreadPool execute our funtions
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        executor.map(get_handles, grade_list, browsers)

# Create Main Function
def main(gradeList):
    # Run our Python Program
    createSourceDir()

    # Testing Functions
    # get_handles("291", headlessBrowser("291"))
    # parseListed("303")
    # parseGoodResults("303")
    
    # Get Data
    setup_workers(gradeList)

    print('\n\nPrinting Master Watch List: ')
    pp.pprint(MasterDict)

    # Remove our TempFiles directory to save space
    sh.rmtree(TempFilesDir, ignore_errors=True)

# Create a counter to increment results dictionary
resultsCounter = 0

# Results dictionary that will hold our watches
watchListed = {}
MasterDict = {}

# Call Main Function
main(watchgradeList)
