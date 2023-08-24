import customtkinter as ctk
import webbrowser

class CTkLink(ctk.CTkLabel):
   
   def __init__(self, master, text, url, font_size=12, *argv, **kwargs):
      
      self.url = url
      
      font = ctk.CTkFont(size=font_size, underline=True)
            
      super().__init__(master, *argv, text=text, font=font, text_color='#6684ff', cursor='hand2', **kwargs)
      self.bind('<Button-1>', self.open_url)
      
   def open_url(self,event=None):
      
      webbrowser.open_new_tab(self.url)
      self.config(fg = 'purple')