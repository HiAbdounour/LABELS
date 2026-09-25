from rich.theme import Theme
from rich.console import Console
import subprocess,sys
import json
from time import sleep

# IMPORTANT VARIABLES
BOOKNAME = 'labels_book.json'
USER_OS = None
SH_OPTION = None

# READ CONFIG
with open("config.json","r") as file:
    configdata = json.load(file)
LINKED_REPO = configdata["link"]

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

def prerequisities():
    global USER_OS,SH_OPTION
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
        return
    csl.print("GitHub CLI successfully found !",style="success")

    # UPDATE SYNC
    if LINKED_REPO!="":
        csl.print("A linked repo was found on the configuration.\nUpdating your local labels book with changes.",style="normal")
        sync_labels()
    return

def allocator():
    CMDS = {'l':create_book,'c':create_label,'d':delete_label,'r':clone_label,'w':link_repo,'q':look_label}

    # MAIN CODE
    csl.print("""\n[b]What do you want to do ?[/b]
    > create a/look into the labels book (l)
    > search a label into the labels book (q)
    > create a new label in your labels book (c)
    > delete a label from your labels book (d)
    > import (clone) labels from your labels book into a repo (r)
    > link or unlink your labels book to a repo (w)
    > EXIT (e)
    """)
    cx = input()
    if cx.lower in CMDS:
        if cx.lower=='e':
            return
        CMDS[cx.lower]()
    else:
        csl.print("Unrecognised command. Please insert a letter among l,c,d,r,w,e,q",style="error")
        allocator()

# UTILITIES
def create_book(show=True):
    # create or look into the labels book
    try:
        with open(BOOKNAME,'r',encoding='utf-8') as book:
            csl.print("Reading the labels book",style="normal")
            sleep(1)
            data = json.load(book)
        if show:
            for label in data:
                csl.print(f'{label["name"]} | {label["description"]} | {label["color"]}')
        else:
            return data
    except (FileNotFoundError, FileExistsError):
        csl.print("Labels book not found. Creating a new one.")
        sleep(1)
        with open(BOOKNAME,"w",encoding='utf-8') as book:
            json.dump([],book)
        csl.print("Labels book created",style='success')
        if not show:
            return []
    except Exception as e:
        raise e

def create_label():
    # create label DIRECTLY on the labels book
    csl.print('Be aware no checks are made (does exist, color is correct)',style='warning')
    csl.print("Indicate your label name :",end=" ",style="normal")
    n = input()
    csl.print("Indicate your label description :",end=' ',style="normal")
    desc = input()
    csl.print("Indicate your label color : expected format : #xxxxxx",end=' ',style="normal")
    clr = input()
    labels = create_book(False)
    labels.append({'name':n,'description':desc,'color':clr})
    with open(BOOKNAME,'w',encoding='utf-8') as book:
        json.dump(labels,book)
    csl.print(f"Successfully created the label [not normal][label_add]{n}[/label_add][/not normal]",style="normal")
    if LINKED_REPO!="":
        csl.print("Would you like to force-create the label on your linked repo ? (y=yes)",style='bold')
        x = input()
        if x.lower=='y':
            try:
                subprocess.run(f"gh label create {n} -c {clr} -d {desc} -R {LINKED_REPO} --force")
                csl.print("Succeeded",style="success")
            except:
                csl.print("An error occured : the label was not created on the linked repo.\nDo it by hands !",style="error")
    return

def delete_label():
    # delete label DIRECTLY on the labels book
    csl.print("Indicate your label name (case-sensitive) :",end=" ",style="normal")
    n = input()
    labels = create_book(False)
    for i in range(len(labels)):
        if labels[i]['name']==n:
            labels.pop(i)
            break
    else:
        csl.print(f"No label with the name {n} found !",style="error")
        return
    with open(BOOKNAME,'w',encoding='utf-8') as book:
        json.dump(labels,book)
        csl.print(f"Successfully deleted the label [not normal][label_remove]{n}[/label_remove][/not normal]",style="normal")
        if LINKED_REPO!="":
            csl.print("Would you like to force-delete the label on your linked repo ? (y=yes)",style='bold')
            x = input()
            if x.lower=='y':
                try:
                    subprocess.run(f"gh label delete {n} -R {LINKED_REPO} --yes")
                except:
                    csl.print("An error occured : the label was not deleted on the linked repo.\nDo it by hands !",style="error")
    return

def link_repo():
    global LINKED_REPO
    # link or unlink repo
    csl.print("Link with :",end=' ',style='bold')
    refx = input()
    if refx!="":
        csl.print(f"Your local labels book will be synced with {refx}. That means each time you use the labeler, updates will be made automatically.",style='normal')
        csl.print("Write Y if you accept :",end=' ',style='normal')
        if input().lower()=='y':
            LINKED_REPO = refx
            configdata['link'] = refx
            save_config()
        else:
            csl.print('ABORTED\n',style='error')
    else:
        LINKED_REPO = ""
        configdata['link'] = ""
        csl.print("Successfully unlink your labels book.")

def look_label():
    csl.print("Search for :",style="normal",end=" ")
    x = input()
    if LINKED_REPO=="":
        csl.print("No linked repo found. Cannot search a specific label")
        return
    subprocess.run(f"gh label list --search {x} -R {LINKED_REPO}")

def clone_label():
    csl.print("What is your destination repo ?",style="bold")
    target = input()
    csl.print("Would you like to use your linked repo (r) or your local labels book (b) ? Default is local")
    q = input()
    if q=='r':
        csl.print(f"Using {LINKED_REPO} as source for cloning",style='normal')
        sleep(1)
        csl.print("Would you like to keep your existing labels (soft), to overwrite existing labels (hard) or to erase all existing labels (bare) ?")
        ds = input()
        if ds.lower()=='bare':
            bare_clone(target)
        else:
            xy = "-f" if ds.lower()=='hard' else ""
            csl.print(f'Cloning labels from {LINKED_REPO} to {target}',style="normal")
            subprocess.run(f"gh label clone {LINKED_REPO} -R {target} {xy}",shell=SH_OPTION)
    else:
        csl.print("Do you want to override the existing labels ? (y=yes)",end=' ',style="normal")
        xx = "-f" if input().lower()=='y' else ""
        labels = create_book(False)
        csl.print(f'Cloning labels from LOCAL LABELS BOOK to {target}',style="normal")
        for label in labels:
            subprocess.run(f"gh label create {label['name']} -c {label['color']} -d {label['description']} -R {target} {xx}",shell=SH_OPTION)
        csl.print("Note that existing labels on repo that does not match a name from your labels book remains.",style="warning")

    csl.print("Successfully clone labels",style="success")
    return

# DING
def sync_labels():
    subprocess.run(f"gh label list --json name,description,color -R {LINKED_REPO}> t.txt",shell=SH_OPTION)

def bare_clone(target):
    csl.print(f"Erasing all existing labels in {target}",style='normal')
    data = subprocess.run(f"gh label ls --json name -R {target}",shell=SH_OPTION,capture_output=True)
    for label in data:
        subprocess.run(f"gh label delete {label['name']} -R {target} --yes",shell=SH_OPTION)
    csl.print(f'Cloning labels from {LINKED_REPO} to {target}',style="normal")
    subprocess.run(f"gh label clone {LINKED_REPO} -R {target} -f",shell=SH_OPTION)
    return

def save_config():
    if LINKED_REPO!="":
        subprocess.run(f"gh label list --json name,description,color -R {LINKED_REPO} > {BOOKNAME}")


# NORMAL ACTIONS
prerequisities()
allocator()