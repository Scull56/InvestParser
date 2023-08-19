import customtkinter as ctk

import json

from components.SideBar import SideBar
from components.MainView import MainView

from db.init_db import init_db

from utils.window_position import window_center

settings = None

with open('settings.json', 'r', encoding="UTF-8") as file:
   settings = file.read()

settings = json.loads(settings)

ctk.set_appearance_mode(settings['theme'])
ctk.set_widget_scaling(settings['scale'])
ctk.set_default_color_theme("blue")

init_db()

class App(ctk.CTk):
   def __init__(self):
      super().__init__()
      
      # configure window
      self.title("InvestParser")
      self.geometry(window_center(self, 1080, 720))
      
      # grid
      self.grid_columnconfigure(1, weight=1)
      self.grid_rowconfigure(0, weight=1)
      
      # sidebar
      sidebar = SideBar(self)
      sidebar.grid(row=0, column=0, sticky="nsew")
      
      # main area
      mainview = MainView(self)
      mainview.grid(column=1, row=0, sticky="nsew")
   
   def destroy(self):
      
      settings = {
         'theme': ctk.get_appearance_mode(),
         'scale': ctk.ScalingTracker.widget_scaling
      }
      
      settings = json.dumps(settings)
      
      with open("settings.json", "w") as file:
         file.write(settings)
      
      super().destroy()
      
if __name__ == "__main__":
   
    app = App()
    
    app.iconbitmap(default="favicon.ico")
    
    app.mainloop()