import customtkinter as ctk
import threading

class Message(ctk.CTkFrame):
   
   colors = {
      'success': "#29a648",
      'error': "#d03b3b",
      'info': "#3B8ED0",
      'warning': '#baa83f'
   }
   
   def __init__(self, master):
      super().__init__(master)
      
      self.grid(sticky="nsew")
      self.grid_columnconfigure(0, weight=1)
      self.grid_rowconfigure(0, weight=1)
      
      self.isActive = False
      
      self.status_label = ctk.CTkLabel(self, text="", text_color="#DCE4EE")
      self.status_label.grid(row=0, column=0, sticky='w', padx=(7, 0))
      
   def show_message(self, message, style="error"):
      
      if style not in Message.colors:
         raise Exception('need specify "error", "info", "warning" or "success" style param for message')
      
      if self.isActive :
         self.timer.cancel()
      
      bg_color = Message.colors[style]
      
      self.configure(fg_color=bg_color)
      
      self.status_label.configure(text=message)
      
      self.isActive = True
      
      self.timer = threading.Timer(5, self.hide_message)
      self.timer.start()
      
   def hide_message(self):
      
      self.configure(fg_color=ctk.ThemeManager.theme["CTkFrame"]["fg_color"])
      self.status_label.configure(text="")