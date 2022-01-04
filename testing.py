import os
import threading
import shutil as sh
from time import sleep
from pathlib import Path
import concurrent.futures
from random import randint
from bs4 import BeautifulSoup
from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
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
    sleep(randint(1, 10))


def headlessBrowser():
    # Create and launch a FireFox Browser

    # Firefox Proile Location
    firefoxProfile = Path(rf"{currentDir}/FirefoxProfile/EbayProfile/")

    # Use Firefox profile
    fp = wd.FirefoxProfile(firefoxProfile)

    # Ebay Sold Listings URL
    ebay_soldUrl = "https://www.ebay.com/sch/i.html?_odkw=&_ipg=25&_sadis=200&_adv=1&_sop=12&LH_SALE_CURRENCY=0&LH_Sold=1&_osacat=0&_from=R40&_dmd=1&LH_Complete=1&_trksid=m570.l1313&_nkw=replacethisword&_sacat=0"

    # Store options to use in Firefox
    firefoxOptions = Options()

    # Start a headless browser (comment out the below line to view what the browser is doing )
    # firefoxOptions.headless = True

    # Run the browser
    browser = wd.Firefox(fp, executable_path=geckoPath, options=firefoxOptions)
    browser.implicitly_wait(10)
    browser.get(ebay_soldUrl)

    input()

    return browser


def captchaBrowser():
    # Create and launch a FireFox Browser

    # Firefox Proile Location
    firefoxProfile = Path(rf"{currentDir}/FirefoxProfile/EbayProfile/")

    # Use Firefox profile
    fp = wd.FirefoxProfile(firefoxProfile)

    # Ebay Sold Listings URL
    ebay_Url = "https://www.ebay.com"

    # Store options to use in Firefox
    firefoxOptions = Options()

    # Start a headless browser (comment out the below line to view what the browser is doing )
    firefoxOptions.headless = False

    # Run the browser
    browser = wd.Firefox(fp, executable_path=geckoPath, options=firefoxOptions)
    browser.implicitly_wait(10)
    browser.get(ebay_Url)

    # Return the browser to use in Threading
    input("Press Enter when Captcha is Completed...")

    browser.quit()

    return


def perform_actions(watchGrade, browser):
    # Automate the browser using selenium

    # input ebay Search
    search_xpath = '//*[@id="gh-ac"]'
    search_box = browser.find_element_by_xpath(search_xpath)
    search_box.send_keys(Keys.CONTROL + "a")
    search_box.send_keys(Keys.DELETE)

    fool()

    search_box.send_keys(watchGrade)
    search_box.send_keys(Keys.RETURN)

    # change items per page
    items_dropdown = browser.find_element_by_xpath(
        "/html/body/div[5]/div[5]/div[2]/div[1]/div[2]/ul/div[3]/div[2]/div/span[2]/button/span"
    )
    items_dropdown.click()

    fool()

    items_200 = browser.find_element_by_xpath(
        "/html/body/div[5]/div[5]/div[2]/div[1]/div[2]/ul/div[3]/div[2]/div/span[2]/span/ul/li[3]/a/span"
    )
    items_200.click()

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


def parse_sold(watchGrade):
    # Parsing html to get sold prices

    # Create lock for threading
    global lock
    lock = threading.Lock()

    # Get the counter to create dictionary entries
    global resultsCounter

    # Import and rebeautify it
    soup = open(SourceFilesDir + "/" + f"{watchGrade}.html")
    newSoup = BeautifulSoup(soup, "html.parser")

    # Get all Sold Listings Data
    results = newSoup.find_all("div", {"class": "s-item__info clearfix"})

    # With Threading iterate adding sold prices to list and average them
    with lock:
        # list to store sold prices
        gradeSoldPrices = []

        for item in results:
            try:
                soldprice = float(
                    item.find("span", {"class": "s-item__price"})
                    .text.replace("$", "")
                    .replace(",", "")
                    .strip()
                )
                gradeSoldPrices.append(soldprice)

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

    # Counter for while loop
    counter = 0

    # Add open browsers to list to use
    while len(browsers) < workers:
        browsers.append(headlessBrowser())
        counter += 1

    # Using ThreadPool execute our funtions
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        executor.map(get_handles, grade_list, browsers)


def captchaCheck(browser):

    verifySource = browser.page_source

    try:
        soup = BeautifulSoup(verifySource, "html.parser")
        verifyText = soup.find("div", {"id": "areaTitle"}).text
    except:
        return

    if "verify" in verifyText:
        captchaBrowser()
        return
    else:
        return


# Create Main Function
def main(gradeList):
    # Run our Python Program
    createSourceDir()

    # Check for captcha and complete it if required
    captchaCheck(headlessBrowser())

    # Get Data
    setup_workers(gradeList)

    # Print our watch grades with their average prices
    print(watchResults)

    # Remove our SourceFiles directory to save space
    sh.rmtree(SourceFilesDir, ignore_errors=True)


# Add Keywords for Ebay Search
watchgradeList = ["291 elgin", "303 elgin"]

# Create a counter to increment results dictionary
resultsCounter = 0

# Results dictionary that will hold our watch grade with their average price
watchResults = {}

# Call Main Function
main(watchgradeList)
