import customtkinter as ctk
from tkinter import *

import json
import re
import requests


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
      
      def update_search_list(event):
         
         search = self.search_input.get()
         
         if search == "":
            
            self.status_label.show_message('Введите название искомой компании')
            return
            
         result = requests.get(f'https://api.investing.com/api/search/v2/search?q={search}')
         
         variants = json.loads(result.content)
         
         variants = list(filter(lambda item: re.split('/', item["url"])[1] == 'equities', variants["quotes"]))
      
         values = list(map(lambda item: f'({item["symbol"]}) {item["description"]} - {item["flag"]}', variants))
         
         self.data = {}
         
         if len(variants) > 0:
            
            for i, item in enumerate(variants):
               self.data[values[i]] = [item['id'], item['url']]
            
            self.search_input.configure(values=values)
            
            self.search_input._open_dropdown_menu()
            
         else:
            self.status_label.show_message('Не найдено совпадений')
      
      self.search_input = ctk.CTkComboBox(self, values=[""])
      self.search_input.grid(row=1, column=0, padx=(0, 20), sticky='ew')
      self.search_input.bind('<KeyPress-Return>', update_search_list)
      
      add_btn = ctk.CTkButton(self, text="Добавить", command=self.add_company)
      add_btn.grid(row=1, column=1, sticky='ew')
      
   def add_company(self):
      
      try:
         value = self.search_input.get()
         
         if value in self.data:
            
            data = self.data[value]
            
         else:
            
            self.status_label.show_message("Выберите компанию из списка поиска")
            return
         
         self.table.add_company(*data)
         self.status_label.show_message("Компания добавлена", "success")
         
         self.search_input.set("")
         
      except NotFoundCompany:
         self.status_label.show_message("Ошибка: введено неправильное название компании")
      
      except NotFoundParams as error:
         self.status_label.show_message(f"Ошибка: не найдены параметры {', '.join(error.params)}")
         
      except CompanyAlreadyAdded:
         self.status_label.show_message("Компания уже добавлена", 'info')
      
      except Exception as exc:
         self.status_label.show_message("Неизвестная ошибка")
         raise exc()