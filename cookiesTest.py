import os
import pickle
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

    cookies = pickle.load(open(os.path.join(SourceFilesDir, "cookiesNew.pkl"), "rb"))

    for cookie in cookies:
        browser.add_cookie(cookie)

    browser.refresh()

    return browser


def captchaBrowser():
    # Create and launch a FireFox Browser

    # Firefox Proile Location
    firefoxProfile = Path(rf"{currentDir}/FirefoxProfile/EbayProfileold/")

    # Use Firefox profile
    fp = wd.FirefoxProfile(firefoxProfile)

    # Ebay Sold Listings URL
    ebay_Url = "https://www.ebay.com/sch/i.html?_odkw=&_ipg=25&_sadis=200&_adv=1&_sop=12&LH_SALE_CURRENCY=0&LH_Sold=1&_osacat=0&_from=R40&_dmd=1&LH_Complete=1&_trksid=m570.l1313&_nkw=replacethisword&_sacat=0"

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

    pickle.dump(
        browser.get_cookies(),
        open(os.path.join(SourceFilesDir, "cookiesNew.pkl"), "wb"),
    )

    browser.quit()

    return


def main():
    createSourceDir()
    captchaBrowser()
    headlessBrowser()
    input("Did it Work?")


main()
