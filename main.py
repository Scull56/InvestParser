import customtkinter as ctk

import json

from components.SideBar import SideBar
from components.MainView import MainView
from components.InstructionWindow import InstructionWindow
from components.UpdateWindow import UpdateWindow
from components.LogsWindow import LogsWindow

from db.init_db import init_db

from utils.window_position import window_center
from utils.storage import storage

import logging

log_format = "%(asctime)s %(levelname)s %(message)s"
logging.basicConfig(level=logging.INFO, filename="data/app.log", filemode="w", encoding='UTF-8', format=log_format)

settings = None

try:
   with open('data/settings.json', 'r', encoding="UTF-8") as file:
      
      settings = file.read()
      settings = json.loads(settings)
      
except:
   settings = {'theme': 'System', 'scale': 1}

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
      
      # additional windows
      self.instruction_window = None
      self.update_window = None
      self.logs_window = None
      
      storage['app'] = self
   
   def open_update_window(self):
      if self.update_window is None or not self.update_window.winfo_exists():
         self.update_window = UpdateWindow(self)
         self.update_window.focus()
      else:
         self.update_window.focus()
   
   def close_update_window(self):
      if self.update_window is not None or self.update_window.winfo_exists():
         self.update_window.destroy()
   
   def open_instruction_window(self):
      if self.instruction_window is None or not self.instruction_window.winfo_exists():
         self.instruction_window = InstructionWindow(self)
         self.instruction_window.focus()
      else:
         self.instruction_window.focus()
   
   def open_logs_window(self):
      if self.logs_window is None or not self.logs_window.winfo_exists():
         self.logs_window = LogsWindow(self)
         self.logs_window.focus()
      else:
         self.logs_window.focus()
   
   def destroy(self):
      
      settings = {
         'theme': ctk.get_appearance_mode(),
         'scale': ctk.ScalingTracker.widget_scaling
      }
      
      settings = json.dumps(settings)
      
      with open("data/settings.json", "w") as file:
         file.write(settings)
      
      logging.info('Приложение завершило работу')
      
      super().destroy()
      
if __name__ == "__main__":
   
    app = App()
    
    app.iconbitmap(default="favicon.ico")
    
    logging.info('Приложение запущено')
    
    app.mainloop()