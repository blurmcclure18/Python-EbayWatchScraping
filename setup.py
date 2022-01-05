import os
from pathlib import Path
from subprocess import call
import subprocess

# Get Working Directory
currentDir = os.path.dirname(__file__)

# Get Script File for Linux and Windows
bashScript = currentDir + "/SetupScripts/BashScript/setupEnv.sh"
windowsScript = currentDir + "/SetupScripts/WindowsScript/setupEnv.ps1"

if os.name == "nt":
    subprocess.call(windowsScript, shell=True)
else:
    pass

if os.name == "posix":
   subprocess.call(bashScript, shell=True)
else:
    pass

subprocess.call(['python', f"{currentDir}/EbaySold.py"])