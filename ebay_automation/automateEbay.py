from selenium import webdriver as wd
from selenium.webdriver.common import keys
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import threading
import time
import concurrent.futures


def getSoldData(watchGrade):
    # Credentials for ebay
    email = "blurmcclure16@gmail.com"
    password = "ILpeor12!"

    myFirefoxProfile = "/home/alecmcclure/.mozilla/firefox/4bue5rgl.blurmcclure"

    # use firefox profile
    fp = wd.FirefoxProfile(myFirefoxProfile)

    # Ebay URL
    ebay_url = "https://ebay.com"
    ebay_soldUrl = "https://www.ebay.com/sch/i.html?_odkw=&_ipg=25&_sadis=200&_adv=1&_sop=12&LH_SALE_CURRENCY=0&LH_Sold=1&_osacat=0&_from=R40&_dmd=1&LH_Complete=1&_trksid=m570.l1313&_nkw=replacethisword&_sacat=0"

    # create and start firefox browser
    firefoxOptions = Options()

    # start a headless browser (comment out the below line to view what the browser is doing )
    # firefoxOptions.headless = True

    # Run the browser
    browser = wd.Firefox(fp)
    browser.implicitly_wait(10)
    browser.get(ebay_soldUrl)
    # try:
    #    # Press login link on page
    #    login_xpath = "/html/body/header/div[1]/ul[1]/li[1]/span/a"
    #    login_link = browser.find_element_by_xpath(login_xpath)
    #    login_link.click()
    #
    #    # enter email address on login prompt
    #    login_email_xpath = '//*[@id="userid"]'
    #    login_email_textbox = browser.find_element_by_xpath(login_email_xpath)
    #    login_email_textbox.send_keys(email)
    #
    #    # Continue Button
    #    continue_btn_xpath = '//*[@id="signin-continue-btn"]'
    #    btn_press = browser.find_element_by_xpath(continue_btn_xpath)
    #    btn_press.click()
    #
    #    # enter password on login prompt
    #    login_password_xpath = '//*[@id="pass"]'
    #    login_password_textbox = browser.find_element_by_xpath(login_password_xpath)
    #    login_password_textbox.send_keys(password)
    #
    #    # press enter to login
    #    login_password_textbox.send_keys(Keys.RETURN)
    # except:
    #    pass

    # input ebay Search
    search_xpath = '//*[@id="gh-ac"]'
    search_box = browser.find_element_by_xpath(search_xpath)
    search_box.send_keys(Keys.CONTROL + "a")
    search_box.send_keys(Keys.DELETE)
    search_box.send_keys(watchGrade)
    search_box.send_keys(Keys.RETURN)

    # change items per page
    items_dropdown = browser.find_element_by_xpath(
        "/html/body/div[5]/div[5]/div[2]/div[1]/div[2]/ul/div[3]/div[2]/div/span[2]/button/span"
    )
    items_dropdown.click()

    items_200 = browser.find_element_by_xpath(
        "/html/body/div[5]/div[5]/div[2]/div[1]/div[2]/ul/div[3]/div[2]/div/span[2]/span/ul/li[3]/a/span"
    )
    items_200.click()

    # obtain browser tab window
    c = browser.window_handles[0]

    # close browser tab window
    # browser.close()

    # switch to tab browser
    browser.switch_to.window(c)

    # perform action on Ebay tab
    ebay_pagesource = browser.page_source

    with open(f"ebay{watchGrade}.html", "w") as writer:
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


def main(grade_list):
    movement = " movement"
    for n in grade_list:
        parse_sold(getSoldData(n))
    return


test_gradeList = ["(291) elgin", "(303) elgin"]

main(test_gradeList)
