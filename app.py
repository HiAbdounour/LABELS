from tkinter import Tk
from components import *
from scripts import controll,clone_labels

class MainApp(Tk):
    def __init__(self):
        controll()
        super().__init__()
        self.title("LABELS - Clone your GitHub repo labels with ease")
        self.geometry("1000x750")
        self.resizable(width=False,height=False) # should maybe change that later

        self.g1 = Group(self,1,'Choose your source repository','Export labels',True)
        self.g1.pack(pady=2)
        self.g2 = Group(self,2,"Import your labels to your repo",'Clone labels')
        self.g2.pack(pady=2)

        # link the button to the function
        self.g2.ifld.btn.configure(
            command=lambda: clone_labels(self.g1.ifld.tfld,self.g2.ifld.tfld)
        )




if __name__=="__main__":
    app = MainApp()
    app.mainloop()