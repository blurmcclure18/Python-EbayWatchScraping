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
    sleep(randint(1,5))

def testBrowser(watchGrade):
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
    firefoxOptions.headless = True # False for Testing
    
    # Run the browser
    browser = wd.Firefox(executable_path=geckoPath, options=firefoxOptions)

    browser.implicitly_wait(10)
    
    # Set Ebay URL
    captchaUrl = f"https://www.ebay.com/sch/i.html?_odkw=&_ipg=25&_sadis=200&_adv=1&_sop=12&LH_SALE_CURRENCY=0&LH_Sold=1&_osacat=0&_from=R40&_dmd=1&LH_Complete=1&_trksid=m570.l1313&_nkw=replacethistext&_sacat=0"
    ebaySoldUrl = f"https://www.ebay.com/sch/i.html?_odkw=&_ipg=25&_sadis=200&_adv=1&_sop=12&LH_SALE_CURRENCY=0&LH_Sold=1&_osacat=0&_from=R40&_dmd=1&LH_Complete=1&_trksid=m570.l1313&_nkw=elgin+grade+{watchGrade}&_sacat=0"
    
    browser.get(ebaySoldUrl)

    return browser

def ebayBrowser(watchGrade):
    # Create and launch a FireFox Browser
    global captchaDetected

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
    ebayListedUrl = f"https://www.ebay.com/sch/i.html?_from=R40&_nkw=elgin+grade+{watchGrade}+movement&_sacat=0&rt=nc&LH_BIN=1"
    ebaySoldUrl = f"https://www.ebay.com/sch/i.html?_odkw=&_ipg=25&_sadis=200&_adv=1&_sop=12&LH_SALE_CURRENCY=0&LH_Sold=1&_osacat=0&_from=R40&_dmd=1&LH_Complete=1&_trksid=m570.l1313&_nkw=elgin+grade+{watchGrade}&_sacat=0"
    
    browser.get(ebayListedUrl)

    if captchaDetected == True:
        with open(f"{currentDir}/Settings/Cookies/captchaCookies.json", 'r') as cookiesfile:
            cookies = json.load(cookiesfile)
    
        for cookie in cookies:
            browser.add_cookie(cookie)
        
        browser.refresh()
    else:
        pass

    try:
        items_dropdown = browser.find_element(By.XPATH,
            "/html/body/div[5]/div[5]/div[2]/div[1]/div[2]/ul/div[3]/div[2]/div/span[2]/button/span"
        )
        items_dropdown.click()

        browser.implicitly_wait(5)

        items_200 = browser.find_element(By.XPATH,
            "/html/body/div[5]/div[5]/div[2]/div[1]/div[2]/ul/div[3]/div[2]/div/span[2]/span/ul/li[3]/a/span"
        )
        items_200.click()
    except:
        pass

    # Get the page source html
    browser.implicitly_wait(5)
    ebayListed = browser.page_source

    # Parse html into Soup with BeautifulSoup
    listedSoup = BeautifulSoup(ebayListed, "html.parser")

    # Write the Beautified Soup to html file for parsing
    with open(f"{currentDir}/TempFiles/{watchGrade}Listed.html","w") as writer:
        writer.write(str(listedSoup))

    browser.get(ebaySoldUrl)

    browser.implicitly_wait(5)
    
    try:
        items_dropdown = browser.find_element(By.XPATH,
            "/html/body/div[5]/div[5]/div[2]/div[1]/div[2]/ul/div[3]/div[2]/div/span[2]/button/span"
        )
        items_dropdown.click()
        
        browser.implicitly_wait(5)

        items_200 = browser.find_element(By.XPATH,
            "/html/body/div[5]/div[5]/div[2]/div[1]/div[2]/ul/div[3]/div[2]/div/span[2]/span/ul/li[3]/a/span"
        )
        items_200.click()
    except:
        pass

    ebaySold = browser.page_source

    # Parse html into Soup with BeautifulSoup
    soldSoup = BeautifulSoup(ebaySold, "html.parser")

    # Write the Beautified Soup to html file for parsing
    with open(f"{currentDir}/TempFiles/{watchGrade}Sold.html","w") as writer:
        writer.write(str(soldSoup))
    
    browser.quit()

    return

def captchaBrowser(watchGrade):
    # Create and launch a FireFox Browser
    print('\nRunning Captcha Capable Browser...')
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

    # Ebay Sold Listings URL
    captchaUrl = f"https://www.ebay.com/sch/i.html?_odkw=&_ipg=25&_sadis=200&_adv=1&_sop=12&LH_SALE_CURRENCY=0&LH_Sold=1&_osacat=0&_from=R40&_dmd=1&LH_Complete=1&_trksid=m570.l1313&_nkw=replacethistext&_sacat=0"

    ebaySoldUrl = f"https://www.ebay.com/sch/i.html?_odkw=&_ipg=25&_sadis=200&_adv=1&_sop=12&LH_SALE_CURRENCY=0&LH_Sold=1&_osacat=0&_from=R40&_dmd=1&LH_Complete=1&_trksid=m570.l1313&_nkw=elgin+grade+{watchGrade}&_sacat=0"

    # Store options to use in Firefox
    firefoxOptions = Options()

    # Start a browser
    firefoxOptions.headless = False # False to allow user to complete captcha

    # Run the browser
    browser = wd.Firefox(executable_path=geckoPath, options=firefoxOptions)
    browser.implicitly_wait(10)
    browser.get(captchaUrl)

    input("Press Enter when Captcha is Completed...")

    browser.implicitly_wait(10)

    with open(f'{currentDir}/Settings/Cookies/captchaCookies.json', 'w') as filehandler:
        json.dump(browser.get_cookies(), filehandler)
            
    browser.quit()

    return browser

def captchaCheck(browser):
    # Run a captcha check and launch a non-headless browser to complete it.
    global captchaDetected
   
    verifySource = browser.page_source
    browser.quit()

    print('\nRunning Captcha Check...')

    try:
        soup = BeautifulSoup(verifySource, "html.parser")
        verifyText = soup.find("div", {"id": "areaTitle"}).text
        
        if "verify" in verifyText:
            print('\nCaptcha Detected Starting Captcha Capable Browser...')
            captchaDetected = True
            captchaBrowser()
        else:
            print('\nNo Captcha Detected...')
    except:
        pass

def parseData(watchGrade):
    # Parse Data based on Sold or Listed Status
    
    # Create lock for threading
    lock = threading.Lock()

    with lock:
        # Import and rebeautify it
        soldSoup = open(f"{currentDir}/TempFiles/{watchGrade}Sold.html","r")
        newSoldSoup = BeautifulSoup(soldSoup, "html.parser")

        # Get all Sold Listings Data
        soldResults = newSoldSoup.find_all("div", {"class": "s-item__info clearfix"})
        
        # list to store sold prices
        gradeSoldPrices = []

        for item in soldResults:
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

        # Results dictionary that will hold our watch grade with their average price
        watchResults = {}
        soldCounter = 0

        # Add the watch grade and average price to dictionary
        watchResults[soldCounter] = {
            "grade": watchGrade,
            "averagePrice": averagePrice,
        }

        # Increase counter for next iteration
        soldCounter += 1

        avgPrices = watchResults

        # Results dictionary that will hold our watches
        watchListed = {}
        
        # Import and rebeautify it
        listedSoup = open(f"{currentDir}/TempFiles/{watchGrade}Listed.html","r")
        newListedSoup = BeautifulSoup(listedSoup, "html.parser")
        
        # Get all Listings Data
        listedResults = newListedSoup.find_all('li',{'class': 's-item s-item__pl-on-bottom s-item--watch-at-corner'})
        
        # Get WatchGrade Average Price
        for n in avgPrices:
            if avgPrices[n]['grade'] == watchGrade:
                watchAvg = avgPrices[n]['averagePrice']
            else:
                pass
        
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
                    watchListed[listedCounter] = {
                        "grade": watchGrade,
                        "watch": product,
                    }

                    # Increase counter for next iteration
                    listedCounter += 1
                else:
                    pass
            except:
                pass
        
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
    return

def getHandles(watchGrade):
    # Using threading perform these functions
    ebayBrowser(watchGrade)
    parseData(watchGrade)

def setupWorkers(grade_list):
    # create workers and list to perform threading
    print('\nStarting Workers...')
    workers = len(grade_list)
    
    #browsers = []
    # Add open browsers to list to use
    #while len(browsers) < workers:
    #    for grade in grade_list:
    #        browsers.append(ebayBrowser(grade))
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        executor.map(getHandles, grade_list)

# Create Main Function
def newMain(gradeList):
    #Run our Program
    createSourceDir()

    # Testing Functions

    # Perform a Captcha Check before launching Threaded Browsers
    #captchaCheck(testBrowser(gradeList[0]))

    #Get Data
    setupWorkers(gradeList)

    # Remove our TempFiles directory to save space
    sh.rmtree(TempFilesDir, ignore_errors=True)

MasterDict = {}
captchaDetected = True

# Call Main Function
newMain(watchgradeList)

# Print Final Results
print('\n\nPrinting Master Watch List: ')
pp.pprint(MasterDict)

with open(f'{currentDir}/MasterDict.py','w') as writer:
    writer.write(f'MasterDict = {MasterDict}')