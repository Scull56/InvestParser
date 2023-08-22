import customtkinter as ctk
import logging

from utils.InvestExceptions import *
from utils.storage import storage

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
      
      logging.info('Начало обновления данных')
      
      storage['app'].open_update_window()
         
      try:
         
         errors = self.table.update_data()
         
         storage['app'].close_update_window()
         
         if len(errors['not_found']) == 0 and len(errors['not_params']):
         
            self.status_label.show_message('Обновление данных прошло успешно', 'success')
            
            logging.info('Обновление данных завершено успешно')
            
         else:
            self.status_label.show_message('Обновление завершено, но не все данные обновлены', 'warning')
            
            not_params_maped = map(lambda item: "\n  " + item[0] + ": " + ", ".join(item[1]), errors["not_params"])
            
            companies = f'\n {"Страницы компаний: " + ", ".join(errors["not_found"])}' if len(errors["not_found"]) > 0 else ''
            params = f'\n {"Индикаторы компаний: " + ", ".join(not_params_maped)}' if len(errors["not_params"]) > 0 else ''
            
            logging.warning(f'Обновление завершено, но не были найдены следующие данные:{companies}{params}')
            
      except Exception as exc:
         
         self.status_label.show_message('Неизвестная ошибка')
         logging.exception('Exception')
      
   def delete_company(self):
      
      deleted_companies = self.table.delete_company()
      
      logging.info(f'Удалены компании: {", ".join(deleted_companies)}')