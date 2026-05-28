import subprocess
import sys
from time import sleep
from tkinter import StringVar

USER_OS = None
SH_OPTION = None

def controll():
    """
    All the control steps grouped in one place !

    SPOILER : Lots of print() !
    """
    global USER_OS,SH_OPTION

    print("Hello there and welcome to LABELS")
    sleep(1)
    print("""
        PLEASE BE AWARE that this script will run several commands into your cmd.
        If you feel worried, you can check the full code on GitHub at github.com/HiAbdounour/LABELS,
        especially the file named scripts.py.
    """)
    sleep(5)

    print('\n')
    USER_OS = sys.platform
    SH_OPTION = False
    if USER_OS=='cygwin' or USER_OS=='win32':
        print("""WARNING !\nYou are on a Windows distribution.
To run, this project will use some privileges.
It is highly recommended to check the code before running any script.
If you don't trust this project, please abort this script.
        """)  # reminder for shell=True ==> security considerations in python docs
        sleep(5)
        SH_OPTION = True

    print("\n")
    # Check if GitHub CLI is installed (yep run only with that)
    print("Looking for GitHub CLI ...")
    cli = subprocess.run("gh --help",shell=SH_OPTION,capture_output=True)
    if cli.returncode!=0:
        raise OSError("GitHub CLI is not installed. Please install it before using this app")
    print("GitHub CLI was successfully found !")
    sleep(2)

    print("The main app will pop up...")
    sleep(1)
    return

def clone_labels(inputvar:StringVar,outputvar:StringVar):
    """

    Does the cloning

    """
    ORGN_REPO = inputvar.get()
    DEST_REPO = outputvar.get()

    if ORGN_REPO is not None and DEST_REPO is not None:
        wanna = input("Do you want to get rid of existing labels on your destination repo ? (y) (default : no) ")
        if wanna=='y':
            opt = '--force'
        else:
            opt = ''

        print("")
        clone = subprocess.run(f"gh label clone {ORGN_REPO} --repo {DEST_REPO} {opt}",shell=SH_OPTION,text=True)
        if clone.returncode!=0:
            print('Error while cloning labels')
        else:
            print("Successfully clone labels")