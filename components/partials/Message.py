import customtkinter as ctk
import threading

class Message(ctk.CTkFrame):
   
   def __init__(self, master):
      super().__init__(master)
      
      self.grid(sticky="ew")
      
      self.isActive = False
      
      self.grid_columnconfigure(0, weight=1)
      self.grid_rowconfigure(0, weight=1)
      
      self.status_label = ctk.CTkLabel(self, text="", text_color="#DCE4EE")
      self.status_label.grid(row=0, column=0)
      
   def show_message(self, message, style="error"):
      
      if self.isActive :
         self.timer.cancel()
      
      bg_color = "#d03b3b"
      
      if style == "info":
         bg_color = "#3B8ED0"
      
      if style == "success":
         bg_color = "#248a5e"
      
      self.configure(fg_color=bg_color)
      
      self.status_label.configure(text=message)
      
      self.isActive = True
      
      self.timer = threading.Timer(5, self.hide_message)
      self.timer.start()
      
   def hide_message(self):
      
      self.configure(fg_color=ctk.ThemeManager.theme["CTkFrame"]["fg_color"])
      self.status_label.configure(text="")