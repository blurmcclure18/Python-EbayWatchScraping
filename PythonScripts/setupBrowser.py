import os
import json
from PythonScripts.Settings.initialSetup import initialSetup

# Get Current Working Directory to use in Functions
currentDir = os.path.dirname(__file__)

def loginBrowser():
    from selenium import webdriver as wd
    from selenium.webdriver.firefox.options import Options
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

    return

if initialSetup != True:
    loginBrowser()
    with open(f'{currentDir}/Settings/initialSetup.py', 'w') as writer:
        writer.write('initialSetup = True')
else:
    pass