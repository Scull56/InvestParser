import customtkinter as ctk
from tkinter import StringVar

import threading

from utils.window_position import window_center

class UpdateWindow(ctk.CTkToplevel):
   
   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      
      self.geometry(window_center(self, 200, 100))
      self.title("InvestParser: Обновление данных")
      self.iconbitmap(default='favicon.ico')
      
      def Quit():
         pass
      
      self.protocol("WM_DELETE_WINDOW", Quit)
      
      self.grid_columnconfigure(0, weight=1)
      self.grid_rowconfigure(0, weight=1)
      
      body = ctk.CTkFrame(self, fg_color='transparent')
      body.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
      
      label = ctk.CTkLabel(body, text='Идет обновление данных')
      label.grid(row=0, column=0, sticky="w")
      
      self.loader_text = StringVar(value='.')
      loader = ctk.CTkLabel(body, textvariable=self.loader_text, font=(ctk.ThemeManager.theme['CTkFont']['family'], 40, 'normal'))
      loader.grid(row=1, column=0, sticky="w")
      
      self.timer = threading.Timer(1, self.update_loader)
      self.timer.start()
      
      self.grab_set()
      
   def update_loader(self):
      
      if len(self.loader_text.get()) < 15:
      
         self.loader_text.set(self.loader_text.get() + '.')
      
      else: 
         
         self.loader_text.set('.')
         
      self.timer = threading.Timer(1, self.update_loader)
      self.timer.start()
   
   def close_window(self):
      
      self.timer.cancel()
      
      self.destroy()