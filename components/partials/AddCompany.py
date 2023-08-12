import customtkinter as ctk

from utils.InvestExceptions import *

class AddСompany(ctk.CTkFrame):
   
   def __init__(self, master, table, status_label):
      super().__init__(master)
      
      self.table = table
      self.status_label = status_label
      
      self.configure(fg_color="transparent", corner_radius=0)
      self.grid(sticky="ew")
      self.grid_columnconfigure(0, weight=1)
      
      self.label = ctk.CTkLabel(self, text="Добавление новой компании", font=ctk.CTkFont(size=14, weight="bold"))
      self.label.grid(row=0, column=0, pady=(0, 5), sticky="w")
      
      self.title_input = ctk.CTkEntry(self, placeholder_text="Название компании")
      self.title_input.grid(row=1, column=0, padx=(0, 20), sticky='ew')
      
      add_btn = ctk.CTkButton(self, text="Добавить", command=self.add_company)
      add_btn.grid(row=1, column=1, sticky='ew')
   
   def add_company(self):
      
      try:
         self.table.add_company(self.title_input.get())
         self.status_label.show_message("Компания добавлена", False)
         
      except NotFoundCompany:
         self.status_label.show_message("Ошибка: введено неправильное название компании")
         
      except Exception as exc:
         self.status_label.show_message("Неизвестная ошибка")
         raise exc()