from Tkinter import *
import ttk
import tkFont
import random


class App():
    def __init__(self):
        # Window structure
        #
        # tk root
        self.root = Tk()
        self.root.title("Minecraft Server Status")

        # Font definitions
        helv18 = tkFont.Font(family='Helvetica', size=18, weight='bold')
        helv36 = tkFont.Font(family='Helvetica', size=36, weight='bold')

        # main frame
        mainframe = ttk.Frame(self.root, padding="12")
        mainframe.grid(column=0, row=0)

        # Header label describing the window
        ttk.Label(mainframe,
                  text="Server Status",
                  font=helv18).grid(column=1, row=1, sticky=N)

        self.status_text = StringVar()
        self.status_text.set("checking...")
        status = Label(mainframe, foreground="#f00",
                       background="#000000", justify=CENTER,
                       height=1, width=10, font=helv36,
                       textvariable=self.status_text)
        status.grid(column=1, row=2, pady="10")
        status.grid_propagate(0)

        ttk.Style().configure('TButton', foreground='blue', relief=RIDGE)
        action_button = ttk.Button(mainframe, text="Toggle",
                                   padding="6", command=self.action)

        action_button.grid(column=1, row=3, pady=6)
        self.update_status()
        self.root.mainloop()

    def action(self):
        self.status_text.set("action!")

    def update_status(self):
        count = random.randint(1,20)
        self.status_text.set("")
        self.status_text.set("check %d" % count)
        self.root.after(3000, self.update_status)

app=App()
