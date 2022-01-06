import os
import json
from subprocess import call
from selenium import webdriver as wd
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

# Inital Setup (Ebay Login Cookie)
def setupBrowser():
    global geckoPath

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

    global cookiePath
    cookiePath = f"{currentDir}/Settings/Cookies/"

# Browser to login to eBay to collect and write login cookie
def loginBrowser():
    # Create and launch a FireFox Browser
    # Ebay Sold Listings URL
    ebayUrl = f"https://www.ebay.com"

    # Run the browser
    browser = wd.Firefox(executable_path=geckoPath)
    browser.implicitly_wait(10)
    browser.get(ebayUrl)

    input("Press Any key after you log into eBay...")

    with open(os.path.join(cookiePath, 'cookies.json'), 'w') as filehandler:
        json.dump(browser.get_cookies(), filehandler)

    browser.quit()

    return

# Create Main Function
def main():
    global initialSetup

    # Run our Python Program
    if initialSetup != True:
        setupPython()
        setupBrowser()
        loginBrowser()
        with open(f'{currentDir}/Settings/initialSetup.py', 'w') as writer:
            writer.write('initialSetup = True')
    else:
        pass
    # Testing Functions

# Add Keywords for Ebay Search in other programs
watchgradeList = ["291"]#, "95"]

# Call Main Function
main()