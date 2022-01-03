from selenium import webdriver as wd
from selenium.webdriver.common import keys
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from time import sleep
from bs4 import BeautifulSoup
import threading
import time
import concurrent.futures
from random import randint

from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# Credentials for pocketwatchdb
email = "blurmcclure16@gmail.com"
password = "0Running!"

myResults = {}


def setup_fx_driver(watchGrade):

    myFirefoxProfile = "/home/alecmcclure/.mozilla/firefox/4bue5rgl.blurmcclure"

    # use firefox profile
    fp = wd.FirefoxProfile(myFirefoxProfile)

    # pocketwatchdb test url
    url = "https://pocketwatchdatabase.com/guide/company/elgin/grade/{}/value"

    # create and start firefox browser
    firefoxOptions = Options()

    # start a headless browser (comment out the below line to view what the browser is doing )
    # firefoxOptions.headless = True

    # Add any options to the browser
    # fp.set_preference("general.useragent.override", myFirefoxProfile)

    # Run the browser
    browser = wd.Firefox(fp)
    browser.implicitly_wait(10)
    browser.get(url.format(watchGrade))

    return browser


def perform_Actions(driver):

    # Press login link on page
    login_xpath = "/html/body/div[2]/div[1]/div/div/div[2]/div[2]/div[1]/table/tbody/tr[1]/td[2]/h6/a/u"
    login_link = driver.find_element_by_xpath(login_xpath)
    login_link.click()

    # enter email address on login prompt
    login_email_xpath = (
        "/html/body/div[4]/div/div/div[2]/div/div[1]/form/div/div[1]/input"
    )
    login_email_textbox = driver.find_element_by_xpath(login_email_xpath)
    login_email_textbox.send_keys(email)

    # enter password on login prompt
    login_password_xpath = (
        "/html/body/div[4]/div/div/div[2]/div/div[1]/form/div/div[2]/input"
    )
    login_password_textbox = driver.find_element_by_xpath(login_password_xpath)
    login_password_textbox.send_keys(password)

    # press enter to login
    login_password_textbox.send_keys(Keys.RETURN)

    # xpath for ebay button
    ebay_xpath = "/html/body/div[2]/div[1]/div[1]/div/div[2]/div[2]/div/div[4]/table/tbody/tr[3]/td[2]/a"

    # Open Ebay link on page
    button = driver.find_element_by_xpath(ebay_xpath)
    sleep(randint(5, 12))
    button.send_keys(Keys.CONTROL + Keys.RETURN)

    # obtain browser tab window
    c = driver.window_handles[1]

    # close browser tab window
    driver.close()

    # switch to tab browser
    driver.switch_to.window(c)

    # perform action on Ebay tab
    driver.implicitly_wait(10)
    ebay_pagesource = driver.page_source

    with open("ebaySource.html", "w") as writer:
        writer.write(ebay_pagesource)

    # Close the browser
    # browser.quit()

    soup = BeautifulSoup(ebay_pagesource, "html.parser")
    return soup


def parse_sold(soups_dict):
    print("\nSold Listing Results: ")
    results = soups_dict.find_all("div", {"class": "s-item__info clearfix"})
    print(len(results))
    return


def get_handles(driver):

    login_xpath = "/html/body/div[2]/div[1]/div/div/div[2]/div[2]/div[1]/table/tbody/tr[1]/td[2]/h6/a/u"

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, login_xpath))
    )

    parse_sold(perform_Actions(driver))


def setup_workers(grade_list):

    workers = len(grade_list)

    drivers = []
    counter = 0
    # drivers = [setup_fx_driver(grade_list) for _ in range(workers)]
    while len(drivers) < workers:
        drivers.append(setup_fx_driver(grade_list[counter]))
        counter += 1

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        executor.map(get_handles, drivers)

    # [driver.quit() for driver in drivers]


test_gradeList = ["291", "303"]
test_grade = "291"
setup_workers(test_gradeList)
# setup_fx_driver(test_gradeList)

# parse_sold(perform_Actions(setup_fx_driver(test_grade)))

# print(perform_Actions(setup_fx_driver(test_grade)))
