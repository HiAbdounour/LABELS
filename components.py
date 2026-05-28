"""
This file stores all custom classes build for
the design of the app (frontend)
"""

import tkinter as tk

# ================================================
#                  SECTION TITLES
# ================================================

class Number(tk.Canvas):
    """
    Manages the number's frame
    """
    def __init__(self,parent,nb):
        super().__init__(parent, width=100, height=100, highlightthickness=0)
        self.width = 100
        self.height = 100
        self.create_text(50,50,text=nb,font='Helvetica 48 bold')
        self.create_oval(99,99,1,1,width=2)
        self.update()

class NumberSection(tk.Frame):
    """
    Build the title of a section
    with a title text and a title number
    """
    def __init__(self,parent,nb,txt):
        super().__init__(parent)
        self.borderwidth = 2
        self.relief = 'GROOVE'
        self.height = 100
        self.width = 800
        self.add_number(nb)
        self.affiliate_text = txt
        self.affiliation()

    def add_number(self,nb):
        Number(self,nb).pack(side='left')

    def affiliation(self):
        label = tk.Label(self,text=self.affiliate_text,font="Helvetica 38 bold")
        label.pack(side='right',expand=True,fill="x",padx=8)

# ================================================
#                INPUT AND BUTTONS
# ================================================

class TextField(tk.Entry):
    """
    Just an input field for text
    """
    def __init__(self,parent):
        self.textvariable = tk.StringVar()
        super().__init__(parent,width=500,font="Helvetica 22",textvariable=self.textvariable)
        self.borderwidth = 2

class Button(tk.Button):
    """
    A simple instance of a button
    """
    def __init__(self,parent,txt):
        super().__init__(parent,text=txt,font='Helvetica 12 bold',bg='lightblue',fg='gray')
        ####### self.command

class InputField(tk.Frame):
    """
    A frame that associates a TextField with a Button
    """
    def __init__(self,parent,btn_txt,disabled):
        super().__init__(parent,width=600)
        self.tfld = None
        self.btn = None
        self.build_field()
        if not disabled:
            self.create_btn(btn_txt)

    def build_field(self):
        self.tfld = TextField(self)
        self.tfld.pack()
    def create_btn(self,txt):
        self.btn = Button(self,txt)
        self.btn.pack()

# ================================================
#                CENTRAL GROUP
# ================================================

class Group(tk.Frame):
    """
    Groups all assets related to one section

    Includes :
    + a NumberSection (with title and number)
    + a InputField (with text input and button)
    """
    def __init__(self,parent,nb,desc,btn_txt,disabled=False):
        super().__init__(parent)
        NumberSection(self,nb,desc).pack()
        self.ifld = InputField(self,btn_txt,disabled)
        self.ifld.pack()
