import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

from components.SideBar import SideBar
from components.MainView import MainView

from db.init_db import init_db

ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

init_db()

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
         
        # configure window
        self.title("InvestParser")
        
        # width and height of modal window
        w = 1080
        h = 720
        
        # get screen width and height
        ws = self.winfo_screenwidth() # width of the screen
        hs = self.winfo_screenheight() # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)

        # set the dimensions of the screen 
        # and where it is placed
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        
        # grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # sidebar
        sidebar = SideBar(self)
        sidebar.grid(row=0, column=0, sticky="nsew")
        
        # main area
        mainview = MainView(self)
        mainview.grid(column=1, row=0, sticky="nsew")

if __name__ == "__main__":
   
    app = App()
    
    app.iconbitmap(default="favicon.ico")
    
    app.mainloop()