import customtkinter as ctk

class CTkText(ctk.CTkLabel):
   
   def __init__(self, master, text, wraplength=500, *args, **kwargs):
      
      super().__init__(master, *args, text=text, wraplength=wraplength, justify='left', **kwargs)