import os
import json
import time
import requests
import pprint as pp
from bs4 import BeautifulSoup
from requests.models import Response
from selenium import webdriver as wd
from Settings.api_key import api_key
from Settings.headless import headless
from selenium.webdriver.common.by import By
from twocaptcha import TwoCaptcha, solver
from selenium.webdriver.firefox.options import Options


currentDir = os.path.dirname(__file__)
TempFilesDir = f"{currentDir}/TempFiles"

ebayCaptchaURL = "https://www.ebay.com/splashui/captcha?ap=1&appName=orch&ru="

pageurl = "https://www.ebay.com/sch/i.html?_odkw=&_ipg=25&_sadis=200&_adv=1&_sop=12&LH_SALE_CURRENCY=0&LH_Sold=1&_osacat=0&_from=R40&_dmd=1&LH_Complete=1&_trksid=m570.l1313&_nkw=replacethistext&_sacat=0"

def requestsCaptcha():
    captchaDetected = False

    r = requests.get(pageurl)

    print('\nRunning Captcha Check...\n')
    verifySource = r.text

    try:
        soup = BeautifulSoup(verifySource, "html.parser")
        verifyText = soup.find("div", {"id": "areaTitle"}).text

        if "verify" in verifyText:
            print('\nCaptcha Detected...\n')
            siteKey = soup.find('input')['value']

            site = soup.find('div', {'class', 'grid-cntr'}).findAll('input', {'name':'ru'})
            siteValStr = str(site[0]).split(" ")[-1]
            link = str(siteValStr).split('"')[1]

            form = {"method": "hcaptcha",
            "sitekey": siteKey,
            "key": api_key,
            "pageurl": f"{ebayCaptchaURL}{link}",
            "json": 1
            }

            captchaResponse = requests.post('http://2captcha.com/in.php', data=form)
            captchaRequestId = Response.json()['request']

            url = f"http://2captcha.com/res.php?key={api_key}&action=get&id={captchaRequestId}&json=1"

            status = 0
            while not status:
                res = requests.get(url)
                if res.json()['status']==0:
                    time.sleep(3)
                else:
                    requ = res.json()['request']
                    js = f'document.getElementById("g-recaptcha-response").innerHTML="{requ}";'
                    driver.execute_script(js)
                    driver.find_element_by_id("recaptcha-demo-submit").submit()
                    status = 1

        else:
            print('\nNo Captcha Detected...')
    except:
        pass



def ebayBrowser(searchTerm):
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
    if headless == True:
        firefoxOptions.headless = True
    else:
        firefoxOptions.headless = False
    
    # Run the browser
    browser = wd.Firefox(executable_path=geckoPath, options=firefoxOptions)

    browser.implicitly_wait(10)
    
    # Set Ebay URL
    inUrlSearch = searchTerm.replace(' ', '+')
    ebayUrl = 'https://ebay.com'
    ebaySoldUrl = "https://www.ebay.com/sch/i.html?_odkw=&_ipg=25&_sadis=200&_adv=1&_sop=12&LH_SALE_CURRENCY=0&LH_Sold=1&_osacat=0&_from=R40&_dmd=1&LH_Complete=1&_trksid=m570.l1313&_nkw=replacethistext&_sacat=0"#f"https://www.ebay.com/sch/i.html?_odkw=&_ipg=25&_sadis=200&_adv=1&_sop=12&LH_SALE_CURRENCY=0&LH_Sold=1&_osacat=0&_from=R40&_dmd=1&LH_Complete=1&_trksid=m570.l1313&_nkw={inUrlSearch}&_sacat=0"

    #browser.get(ebayUrl)

    #browser.implicitly_wait(5)
     
    #with open(f"{currentDir}/Settings/Cookies/loginCookies.json", 'r') as cookiesfile:
    #    cookies = json.load(cookiesfile)
    #
    #for cookie in cookies:
    #    browser.add_cookie(cookie)
    #browser.refresh()

    browser.get(ebaySoldUrl)

    browser.implicitly_wait(5)

    verifySource = browser.page_source
    
    print('\nRunning Captcha Check...\n')
    try:
        soup = BeautifulSoup(verifySource, "html.parser")
        verifyText = soup.find("div", {"id": "areaTitle"}).text

        if "verify" in verifyText:
            print('\nCaptcha Detected...\n')
            captchaDetected = True
            time.sleep(5)
        else:
            print('\nNo Captcha Detected...')
    except:
        pass

    if captchaDetected == True:
        print('\nResolving Captcha')
        solver = TwoCaptcha(api_key)
        siteKey = soup.find('input')['value']
        site = soup.find('div', {'class', 'grid-cntr'}).findAll('input', {'name':'ru'})
        siteValStr = str(site[0]).split(" ")[-1]
        link = str(siteValStr).split('"')[1]

        result = solver.hcaptcha(sitekey=siteKey, url='https://www.ebay.com/splashui/captcha?ap=1',)
        print(result)
    else:
        pass
    #try:
    #    items_dropdown = browser.find_element(By.XPATH,
    #        "/html/body/div[5]/div[5]/div[2]/div[1]/div[2]/ul/div[3]/div[2]/div/span[2]/button/span"
    #    )
    #    items_dropdown.click()

    #    sleep(randint(2,5))
    #    
    #    browser.implicitly_wait(5)

    #    items_200 = browser.find_element(By.XPATH,
    #        "/html/body/div[5]/div[5]/div[2]/div[1]/div[2]/ul/div[3]/div[2]/div/span[2]/span/ul/li[3]/a/span"
    #    )
    #    items_200.click()
    #except:
    #    pass

    #ebaySold = browser.page_source

    ## Parse html into Soup with BeautifulSoup
    #soldSoup = BeautifulSoup(ebaySold, "html.parser")

    ## Write the Beautified Soup to html file for parsing
    #with open(f"{currentDir}/TempFiles/{searchTerm}Sold.html","w") as writer:
    #    writer.write(str(soldSoup))
    
    input('\nDid it work?')

    browser.refresh()

    #browser.quit()

ebayBrowser('nothing')