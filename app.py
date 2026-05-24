from tkinter import Tk
from components import *

class MainApp(Tk):
    def __init__(self):
        super().__init__()
        self.title("LABELS - Clone your GitHub repo labels with ease")
        self.geometry("1000x750")
        self.resizable(width=False,height=False) # should maybe change that later

        Group(self,1,'Choose your source repository','Export labels').pack(pady=2)
        Group(self,2,"Import your labels to your repo",'Import labels').pack(pady=2)




if __name__=="__main__":
    app = MainApp()
    app.mainloop()