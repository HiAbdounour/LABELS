from rich.theme import Theme
from rich.console import Console
import subprocess
import sys
from time import sleep

# DEFINING RICH STYLES
them = Theme({
    "normal": "default on default",
    "success": "green",
    "warning": "yellow",
    "error": "bold red",
    "label_info": "black on white", # will probably not use that
    "label_add": "green on white",
    "label_remove": "red strike on white"
})
csl = Console(theme=them)

# STARTING POINT
csl.print("Welcome to interactive labeler LABELS",style="normal")
sleep(1)
csl.print("[b]Note to the user :[/b]",style='normal')
csl.print("""
BE AWARE this script will run several commands into your terminal.
If you feel worried, you can check the full code on GitHub at github.com/HiAbdounour/LABELS
""",style="warning")
sleep(4)

# DETECTING OS
USER_OS = sys.platform
SH_OPTION = (USER_OS=='cygwin' or USER_OS=='win32')
if SH_OPTION:
    csl.print("[b]Warning ![/b]",style="warning")
    csl.print("""You are on a Windows distribution.
To run, the current code will use some privileges.
It is highly recommended to check the code and to ensure its integrity before running any script.
If you don't trust this project, please abort this script.
""",style="warning") # reminder for shell=True ==> security considerations in python docs
    sleep(5)
sleep(0.5)

# LOOKING FOR GITHUB CLI
csl.print("Looking for GitHub CLI ...",style="normal")
cli = subprocess.run("gh --help",shell=SH_OPTION,capture_output=True)
sleep(1)
if cli.returncode!=0:
    csl.print("ERROR ! GitHub CLI was not found on your machine !",style="error")
    csl.print("The Labeler cannot (yet) install GitHub CLI itself. You must install it yourself.")
    raise RuntimeError("Abort programm : GitHub CLI") # evolve this shit
csl.print("GitHub CLI successfully found !",style="success")


