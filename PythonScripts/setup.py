import os
import json
from subprocess import call
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
    windowsScript = f"{currentDir}/SetupScripts/WindowsScript/setupEnv.ps1"
    
    if os.name == "nt":
        call(windowsScript, shell=True)
    else:
        pass
    if os.name == "posix":
        call(bashScript, shell=True)
    else:
        pass

# Browser to login to eBay to collect and write login cookie
def captchaBrowser():
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

    # Ebay Captcha URL
    captchaUrl = f"https://www.ebay.com/sch/i.html?_odkw=&_ipg=25&_sadis=200&_adv=1&_sop=12&LH_SALE_CURRENCY=0&LH_Sold=1&_osacat=0&_from=R40&_dmd=1&LH_Complete=1&_trksid=m570.l1313&_nkw=replacethistext&_sacat=0"

    # Store options to use in Firefox
    firefoxOptions = Options()

    # Start a headless browser (comment out the below line to view what the browser is doing )
    firefoxOptions.headless = False

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

# Create Main Function
def main():
    global initialSetup

    # Run our Python Program
    if initialSetup != True:
        setupPython()
        captchaBrowser()

        with open(f'{currentDir}/Settings/initialSetup.py', 'w') as writer:
            writer.write('initialSetup = True')
    else:
        pass

# Add Keywords for Ebay Search in other programs
watchgradeList = ["95", "291", "303"]

# Call Main Function
main()