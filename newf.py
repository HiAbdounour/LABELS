from rich.theme import Theme
from rich.console import Console
import subprocess
import sys
from time import sleep

# IMPORTANT FLAGS
USER_OS = None
SH_OPTION = None

# Rich styles
them = Theme({
    "normal": "default on default",
    "warning": "yellow",
    "error": "bold red",
    "label_info": "black on white", # will probably not use that
    "label_add": "green on white",
    "label_remove": "red strike on white"
})
csl = Console(theme=them)


