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

currentDir = os.path.dirname(__file__)
SourceFiles = "SourceFiles"

SourceFilesDir = currentDir + '/' + SourceFiles

def createSourceDir():
    try:
        os.mkdir(SourceFiles)
    except:
        pass


def fool():
    sleep(randint(1,10))

def setupBrowser():
    
    #myFirefoxProfile = Path(r'/home/alec/Documents/GitHub/Python-EbayAPI/FirefoxProfile/ebayProfile')
    firefoxProfile = Path(rf"{currentDir}/FirefoxProfile/EbayProfile/")

    # use firefox profile
    fp = wd.FirefoxProfile(firefoxProfile)

    # Ebay URL
    ebay_soldUrl = "https://www.ebay.com/sch/i.html?_odkw=&_ipg=25&_sadis=200&_adv=1&_sop=12&LH_SALE_CURRENCY=0&LH_Sold=1&_osacat=0&_from=R40&_dmd=1&LH_Complete=1&_trksid=m570.l1313&_nkw=replacethisword&_sacat=0"

    # create and start firefox browser
    firefoxOptions = Options()

    # start a headless browser (comment out the below line to view what the browser is doing )
    firefoxOptions.headless = True

    # Run the browser
    browser = wd.Firefox(fp, options=firefoxOptions)
    browser.implicitly_wait(10)
    browser.get(ebay_soldUrl)

    return browser


def perform_actions(watchGrade, browser):

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

    # perform action on Ebay tab
    ebay_pagesource = browser.page_source
    
    # Close the browser
    browser.quit()

    soup = BeautifulSoup(ebay_pagesource, "html.parser")

    newSoup = soup
    soup.find("div", {'class': 'srp-merch__items clearfix'}).decompose()
    
    with open(os.path.join(SourceFilesDir, watchGrade + ".html"),'w') as writer:
        writer.write(str(newSoup))

def parse_sold(watchGrade):
    global lock
    lock = threading.Lock()

    global resultsCounter

    soup = open(SourceFilesDir + '/' + f'{watchGrade}.html')
    newSoup = BeautifulSoup(soup, 'html.parser')
    results = newSoup.find_all('div', {'class': 's-item__info clearfix'})

    numResults = len(results)

    with lock:
        
        gradeSoldPrices = []
        
        for item in results:
            try:
                soldprice =  float(item.find('span', {'class': 's-item__price'}).text.replace('$',"").replace(',','').strip())
                gradeSoldPrices.append(soldprice)
            
            except:
                pass
        
        averagePrice = round(sum(gradeSoldPrices) / len(gradeSoldPrices))
        
        myResults[resultsCounter] = {'grade': watchGrade, 'averagePrice':averagePrice}
        resultsCounter += 1

def get_handles(watchGrade, browser):
    
    perform_actions(watchGrade, browser)

    parse_sold(watchGrade)

def setup_workers(grade_list):
    
    workers = len(grade_list)
    browsers = []
    counter = 0
    
    while len(browsers) < workers:
        browsers.append(setupBrowser())
        counter += 1

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        executor.map(get_handles, grade_list, browsers)

def main(gradeList):

    createSourceDir()

    setup_workers(gradeList)
    
    print(myResults)
    
    sh.rmtree(SourceFilesDir, ignore_errors=True)

watchgradeList = ["291 elgin", "303 elgin"]

resultsCounter = 0
myResults = {}

main(watchgradeList)