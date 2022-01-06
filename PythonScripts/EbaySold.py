import os
import json
import threading
import shutil as sh
from time import sleep
from pathlib import Path
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

def foolU():
    sleep(randint(2,12))

def createSourceDir():
    # Create the folder to store temp html files
    try:
        os.mkdir(f"{currentDir}/TempFiles")
    except:
        pass

def headlessBrowser(watchGrade):
    # Create and launch a FireFox Browser

    # Ebay Sold Listings URL
    ebayUrl = "https://www.ebay.com/"
    ebaySoldUrl = f"https://www.ebay.com/sch/i.html?_odkw=&_ipg=25&_sadis=200&_adv=1&_sop=12&LH_SALE_CURRENCY=0&LH_Sold=1&_osacat=0&_from=R40&_dmd=1&LH_Complete=1&_trksid=m570.l1313&_nkw=elgin+grade+{watchGrade}&_sacat=0"

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

    browser.get(ebayUrl)

    with open(f"{currentDir}/Settings/Cookies/cookies.json", 'r') as cookiesfile:
        cookies = json.load(cookiesfile)
    
    for cookie in cookies:
        browser.add_cookie(cookie)
    
    browser.refresh()

    foolU()

    browser.get(ebaySoldUrl)

    return browser

def perform_actions(watchGrade, browser):
    # Automate the browser using selenium

    # Change items per page
    browser.implicitly_wait(10)
    
    try:
        items_dropdown = browser.find_element(By.XPATH,
            "/html/body/div[5]/div[5]/div[2]/div[1]/div[2]/ul/div[3]/div[2]/div/span[2]/button/span"
        )
        items_dropdown.click()

        foolU()

        items_200 = browser.find_element(By.XPATH,
            "/html/body/div[5]/div[5]/div[2]/div[1]/div[2]/ul/div[3]/div[2]/div/span[2]/span/ul/li[3]/a/span"
        )
        items_200.click()
    except:
        pass

    # Get the page source html
    browser.implicitly_wait(10)
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

def parse_sold(watchGrade):
    # Parsing html to get sold prices

    # Create lock for threading
    global lock
    lock = threading.Lock()

    # Get the counter to create dictionary entries
    global resultsCounter

    # Import and rebeautify it
    soup = open(f"{currentDir}/TempFiles/{watchGrade}.html","r")
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

def get_handles(watchGrade, browser):
    # Using threading perform these funtions

    perform_actions(watchGrade, browser)

    parse_sold(watchGrade)


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
    # headlessBrowser()
    # get_handles('291', headlessBrowser('291'))

    # Get Data
    setup_workers(gradeList)

    # Print our watch grades with their average prices
    with open(os.path.join(currentDir, "watchAvgPrices.py"), "w") as writer:
        writer.write(f"avgPrices = {watchResults}")

    # Remove our TempFiles directory to save space
    sh.rmtree(TempFilesDir, ignore_errors=True)

# Create a counter to increment results dictionary
resultsCounter = 0

# Results dictionary that will hold our watch grade with their average price
watchResults = {}

# Call Main Function
main(watchgradeList)