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


def getSoldData(watchGrade):
    # Credentials for pocketwatchdb
    email = "blurmcclure16@gmail.com"
    password = "0Running!"

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

    # Press login link on page
    login_xpath = "/html/body/div[2]/div[1]/div/div/div[2]/div[2]/div[1]/table/tbody/tr[1]/td[2]/h6/a/u"
    login_link = browser.find_element_by_xpath(login_xpath)
    login_link.click()

    # enter email address on login prompt
    login_email_xpath = (
        "/html/body/div[4]/div/div/div[2]/div/div[1]/form/div/div[1]/input"
    )
    login_email_textbox = browser.find_element_by_xpath(login_email_xpath)
    login_email_textbox.send_keys(email)

    # enter password on login prompt
    login_password_xpath = (
        "/html/body/div[4]/div/div/div[2]/div/div[1]/form/div/div[2]/input"
    )
    login_password_textbox = browser.find_element_by_xpath(login_password_xpath)
    login_password_textbox.send_keys(password)

    # press enter to login
    login_password_textbox.send_keys(Keys.RETURN)

    # xpath for ebay button
    ebay_xpath = "/html/body/div[2]/div[1]/div[1]/div/div[2]/div[2]/div/div[4]/table/tbody/tr[3]/td[2]/a"

    # Open Ebay link on page
    button = browser.find_element_by_xpath(ebay_xpath)
    sleep(randint(5, 12))
    button.send_keys(Keys.CONTROL + Keys.RETURN)

    # Switch focus to the Ebay tab
    sleep(2)

    # obtain browser tab window
    c = browser.window_handles[1]

    # close browser tab window
    browser.close()

    # switch to tab browser
    browser.switch_to.window(c)

    # perform action on Ebay tab
    browser.implicitly_wait(10)
    ebay_pagesource = browser.page_source

    # Close the browser
    # browser.quit()

    soup = BeautifulSoup(ebay_pagesource, "html.parser")

    return soup


def parse_sold(soups_dict):
    print("\nSold Listing Results: ")
    results = soups_dict.find_all("div", {"class": "s-item__info clearfix"})
    print(len(results))
    return


def main(grade_list):
    for n in grade_list:
        parse_sold(getSoldData(n))
        sleep(randint(2, 15))
    return


test_gradeList = ["291", "303"]

main(test_gradeList)
