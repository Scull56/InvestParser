import customtkinter as ctk

class CTkText(ctk.CTkTextbox):
   
   def __init__(self, master, text, *args, **kwargs):
      
      super().__init__(master, *args, fg_color='transparent', wrap='word', activate_scrollbars=False, **kwargs)
      
      self.insert('end', text=text)
      self.configure(state='disabled')
      self.grid(sticky='nsew')