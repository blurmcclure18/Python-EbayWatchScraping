import os
from subprocess import call
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

if initialSetup != True:
    setupPython()
else:
    pass