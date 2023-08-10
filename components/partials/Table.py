import customtkinter as ctk
from tksheet import Sheet

from modules.CTkTable import CTkTable

class Table(ctk.CTkFrame):
   
   def __init__(self, master):
      super().__init__(master)
      
      self.configure(fg_color="transparent")
      self.grid(sticky="nsew")
      self.grid_rowconfigure(0, weight=1)
      self.grid_columnconfigure(0, weight=1)
      
      ctk.get_appearance_mode()
      
      sheet = CTkTable(self, data = [[f"Row {r}, Column {c}" for c in range(7)] for r in range(30)])
      sheet.headers(["Страна","Сектор","Под сектор","Компания","EBITDA", "Net Profit Margin", "Чекбокс"])
      
      sheet.enable_bindings()
      sheet.disable_bindings(['rc_insert_column', 'rc_delete_column', 'edit_cell', 'delete', 'paste',
                                         'cut', 'rc_delete_row', 'rc_insert_row'])
      
      sheet.grid(row=0, column=0, sticky="nsew")