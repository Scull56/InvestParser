import customtkinter as ctk

from components.UpdateWindow import UpdateWindow

from utils.InvestExceptions import *

class ToolBar(ctk.CTkFrame):
   
   def __init__(self, master, table, status_label):
      super().__init__(master)
      
      self.table = table
      self.status_label = status_label
      
      self.configure(fg_color="transparent")
      
      self.min_resize_value = 0.7
      
      update_data_btn = ctk.CTkButton(self, text="Обновить данные", command=self.update_data)
      update_data_btn.grid(row=0, column=0, padx=(0, 20))
      
      resize_table_btn = ctk.CTkButton(self, text="Изменить масштаб таблицы", command=self.toggle_scale)
      resize_table_btn.grid(row=0, column=1, padx=(0, 20))
      self.resize_value = self.min_resize_value
      
      delete_rows_btn = ctk.CTkButton(self, text="Удалить выделенные", command=self.delete_company)
      delete_rows_btn.grid(row=0, column=2)  
      
   def toggle_scale(self):
      
      self.table.set_scale(self.resize_value)
      
      self.resize_value = 1 if self.resize_value == self.min_resize_value else self.min_resize_value
      
   def update_data(self):
      
      self.update_window = UpdateWindow()
      
      try:
         self.table.update_data()
         self.status_label.show_message('Обновление данных прошло успешно', 'success')
         
      except Exception as exc:
         self.status_label.show_message('Неизвестная ошибка')
         raise exc()
         
      self.update_window.destroy()
      self.update_window = None
      
   def delete_company(self):
      self.table.delete_company()