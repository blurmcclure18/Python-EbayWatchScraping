import os
import json
from subprocess import call
from typing import Counter
from selenium import webdriver as wd
from selenium.webdriver.firefox.options import Options
from PythonScripts.Settings.initialSetup import initialSetup

# Get Current Working Directory to use in Functions
currentDir = os.path.dirname(__file__)

# Create Functions to use in program

# Setup Python using pip in Linux and Windows Scripts
def setupPython():
    # Get Script File for Linux and Windows
    bashScript = f"{currentDir}/SetupScripts/BashScript/setupEnv.sh"
    windowsScript = f"{currentDir}/SetupScripts/WindowsScript/setupEnv.bat"
    
    if os.name == "nt":
        call(windowsScript, shell=True)
    else:
        pass
    if os.name == "posix":
        call(bashScript, shell=True)
    else:
        pass

# Browser to login to eBay to collect and write login cookie
def loginBrowser():
    # Create and launch a FireFox Browser
    print('\nPlease login to Ebay...\n')
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

    # Ebay Captcha URL
    captchaUrl = f"https://www.ebay.com/"

    # Store options to use in Firefox
    firefoxOptions = Options()

    # Start a headless browser (comment out the below line to view what the browser is doing )
    firefoxOptions.headless = False

    # Run the browser
    browser = wd.Firefox(executable_path=geckoPath, options=firefoxOptions)
    browser.implicitly_wait(10)
    browser.get(captchaUrl)

    input("Press Enter when Login is Completed...")

    browser.implicitly_wait(10)

    with open(f'{currentDir}/Settings/Cookies/loginCookies.json', 'w') as filehandler:
        json.dump(browser.get_cookies(), filehandler)
            
    browser.quit()

    return browser

# Create Main Function
def main():
    global initialSetup

    # Run our Python Program
    if initialSetup != True:
        setupPython()
        loginBrowser()

        with open(f'{currentDir}/Settings/initialSetup.py', 'w') as writer:
            writer.write('initialSetup = True')
    else:
        pass
    
    getUserSearch()

# Add Keywords for Ebay Search in other programs
def getUserSearch():

    userDoneFinal = ['',]
    whileCounter = 0
    print(userDoneFinal[whileCounter])
    while userDoneFinal[whileCounter] != 'no':
        searchNameList.append(input('\nCreate a Name for your Search:\n'))
        keywordsList.append(input('\nPlease enter your search term:\n'))
        userDoneFinal.append(input('\nWould you like to add another search?:\n').lower())
        whileCounter += 1


searchNameList = []
keywordsList = []

# Call Main Function
main()