import customtkinter as ctk

from modules.CTkText import CTkText

from modules.CTkLink import CTkLink

from utils.window_position import window_center

class LogsWindow(ctk.CTkToplevel):
   
   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      
      self.geometry(window_center(self, 500, 300))
      self.title("InvestParser: Logs")
      self.wm_iconbitmap(default='favicon.ico')
      
      self.grid_columnconfigure(0, weight=1)
      self.grid_rowconfigure(0, weight=1)
      
      text_box = ctk.CTkTextbox(self)
      text_box.grid(row=0, column=0, sticky='nsew')
      
      with open('data/app.log', 'r', encoding='UTF-8') as file:
         text = file.read()
         text_box.insert('end', text=text)
      
      text_box.configure(state="disabled")
      
      self.grab_set()