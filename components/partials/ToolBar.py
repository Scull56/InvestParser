import customtkinter as ctk

from utils.InvestExceptions import *

class ToolBar(ctk.CTkFrame):
   
   def __init__(self, master, table, status_label):
      super().__init__(master)
      
      self.table = table
      
      self.configure(fg_color="transparent")
      
      update_data_btn = ctk.CTkButton(self, text="Обновить данные", command=self.update_data)
      update_data_btn.grid(row=0, column=0, padx=(0, 20))
      
      resize_table_btn = ctk.CTkButton(self, text="Изменить масштаб таблицы")
      resize_table_btn.grid(row=0, column=1, padx=(0, 20))
      
      delete_rows_btn = ctk.CTkButton(self, text="Удалить выделенные", command=self.delete_company)
      delete_rows_btn.grid(row=0, column=2)
      
   def update_data(self):
      self.table.update_data()
   def delete_company(self):
      self.table.delete_company()