import os
import threading
import shutil as sh
import pprint as pp
from time import sleep
from pathlib import Path
import concurrent.futures
from random import randint
from bs4 import BeautifulSoup
from watchAvgPrices import avgPrices
from selenium import webdriver as wd
from selenium.webdriver.common import by
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

# Get Current Working Directory to use in Functions
currentDir = os.path.dirname(__file__)
SourceFiles = "SourceFiles"
SourceFilesDir = currentDir + "/" + SourceFiles

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
        os.mkdir(SourceFiles)
    except:
        pass


def fool():
    # Using random sleep duration to help fool captcha
    sleep(randint(3, 12))


def headlessBrowser(watchGrade):
    # Create and launch a FireFox Browser

    # Firefox Proile Location
    firefoxProfile = Path(rf"{currentDir}/FirefoxProfile/EbayProfile/")

    # Use Firefox profile
    #fp = wd.FirefoxProfile(firefoxProfile)

    # Ebay Sold Listings URL
    ebayUrl = f"https://www.ebay.com/sch/i.html?_from=R40&_nkw=elgin+grade+{watchGrade}&_sacat=0&rt=nc&LH_BIN=1"

    # Store options to use in Firefox
    firefoxOptions = Options()

    # Start a headless browser (comment out the below line to view what the browser is doing )
    #firefoxOptions.headless = True
    firefoxOptions.profile = firefoxProfile

    # Run the browser
    browser = wd.Firefox(executable_path=geckoPath, options=firefoxOptions)
    browser.implicitly_wait(10)
    browser.get(ebayUrl)

    return browser

def perform_actions(watchGrade, browser):
    # Automate the browser using selenium

    browser.implicitly_wait(10)

    # change items per page
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
    ebay_pagesource = browser.page_source

    # Close the browser
    browser.quit()

   # Parse html into Soup with BeautifulSoup
    soup = BeautifulSoup(ebay_pagesource, "html.parser")

    # Remove "Related Items" section that would give false info
    newSoup = soup
    soup.find("div", {"class": "srp-merch__items clearfix"}).decompose()

    # Write the Beautified Soup to html file for parsing
    with open(os.path.join(SourceFilesDir, watchGrade + ".html"), "w") as writer:
        writer.write(str(newSoup))


def parse_listed(watchGrade):
    # Parsing html to get sold prices

    # Create lock for threading
    global lock
    lock = threading.Lock()

    # Get the counter to create dictionary entries
    global resultsCounter

    # Import and rebeautify it
    soup = open(SourceFilesDir + "/" + f"{watchGrade}.html")
    newSoup = BeautifulSoup(soup, "html.parser")

    # Get all Listings Data
    results = newSoup.find_all("div", {"class": "s-item__info clearfix"})

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

def get_handles(watchGrade, browser):
    # Using threading perform these funtions

    perform_actions(watchGrade, browser)

    parse_listed(watchGrade)


def setup_workers(grade_list):
    # create workers and list to perform threading
    workers = len(grade_list)
    browsers = []

    # Counter for while loop
    counter = 0

    # Add open browsers to list to use
    while len(browsers) < workers:
        for grade in grade_list:
            browsers.append(headlessBrowser(grade))
        counter += 1

    # Using ThreadPool execute our funtions
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        executor.map(get_handles, grade_list, browsers)

# Create Main Function
def main(gradeList):
    # Run our Python Program
    createSourceDir()

    # Testing Functions
    # get_handles("303", headlessBrowser("303"))
    #parse_listed("303")

    # Get Data
    setup_workers(gradeList)

    # Print our watch grades with their average prices
    numResults = len(watchListed)
    print(f'\nNumber of Listed Entries : {numResults}\n')

    print('\n\nPrinting Master Watch List: ')
    pp.pprint(watchListed)

    # Remove our SourceFiles directory to save space
    sh.rmtree(SourceFilesDir, ignore_errors=True)

# Add Keywords for Ebay Search
watchgradeList = ["291", "303", "450"]

# Create a counter to increment results dictionary
resultsCounter = 0

# Results dictionary that will hold our watch grade with their average price
watchListed = {}

# Call Main Function
main(watchgradeList)
