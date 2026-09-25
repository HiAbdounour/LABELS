from rich.theme import Theme
from rich.console import Console
import subprocess
import sys
from time import sleep

# IMPORTANT FLAGS
USER_OS = None
SH_OPTION = None

# DEFINING RICH STYLES
them = Theme({
    "normal": "default on default",
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


