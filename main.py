from Tkinter import *
import ttk
import tkFont
import tkMessageBox
import random
from instance import *


class App():
    def __init__(self):
        try:
            self.instance = EC2Instance()
        except InstanceException, e:
            tkMessageBox.showerror("Error", e.value)
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
        status.grid(column=1, row=2, pady="10", ipady="10")
        status.grid_propagate(0)

        self.button_text = StringVar()
        self.button_text.set("....")
        ttk.Style().configure('TButton', foreground='blue', relief=RIDGE)
        self.action_button = ttk.Button(mainframe,
                                        textvariable=self.button_text,
                                        padding="6", command=self.action)
        self.action_button.grid(column=1, row=3, pady=6)

        self.update_status()
        self.root.mainloop()

    def action(self):
        try:
            result = self.instance.toggle()
            tkMessageBox.showinfo("Status", result)
        except InstanceException, e:
            tkMessageBox.showwarning("Warning", e.value)

    def update_status(self):
        try:
            status = self.instance.status()
            self.status_text.set(status)
            self.update_button(status)
            self.root.after(3000, self.update_status)
        except InstanceException, e:
            tkMessageBox.showerror("Error", e.value)
            exit()

    def update_button(self,status):
        if status == "running":
            self.button_text.set("Stop Server")
            self.action_button.state(["!disabled"])
        elif status == "stopped":
            self.button_text.set("Start Server")
            self.action_button.state(["!disabled"])
        else:
            self.button_text.set("Wait")
            self.action_button.state(["disabled"])
            


app=App()
