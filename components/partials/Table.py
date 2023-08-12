import customtkinter as ctk

from modules.CTkTable import CTkTable

from utils.InvestExceptions import *

from parsers.InvestParser import InvestParser

from db.commands import (
   get_companies,
   add_company as db_add
)

class Table(ctk.CTkFrame):
   
   def __init__(self, master):
      super().__init__(master)
      
      self.configure(fg_color="transparent")
      self.grid(sticky="nsew")
      self.grid_rowconfigure(0, weight=1)
      self.grid_columnconfigure(0, weight=1)
      
      ctk.get_appearance_mode()
      
      companies = get_companies()
      data = []
      
      for item in companies:
         data.append([item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9], item[10], item[11], item[12], item[13]])
      
      self.sheet = CTkTable(self,
                            data=data,
                            header_align='w',
                            header_height="1",
                            column_width=120,
                            row_height=75)
      
      self.sheet.headers(["Страна","Индустрия","Сектор","Компания","EBITDA млрд", "Net Profit Margin", "P/E", "P/S", "Diluted EPS", "ROE", "ROA", "Debt/Equity", "Технический анализ"])

      self.sheet.enable_bindings()
      self.sheet.disable_bindings(['rc_insert_column', 'rc_delete_column', 'edit_cell', 'delete', 'paste',
                                         'cut', 'rc_delete_row', 'rc_insert_row', "edit_index", "edit_header", "drag",
                                         'column_drag_and_drop', "row_drag_and_drop" ])
      
      self.sheet.grid(row=0, column=0, sticky="nsew")
      
      self.sheet.create_header_dropdown(c = 0,
                                       values = ["all", "1", "2", "3"],
                                       set_value = "all",
                                       selection_function = self.header_dropdown_selected,
                                       text = "Страна")
      self.sheet.create_header_dropdown(c = 1,
                                       values = ["all", "a", "b", "c"],
                                       set_value = "all",
                                       selection_function = self.header_dropdown_selected,
                                       text = "Индустрия")
      self.sheet.create_header_dropdown(c = 2,
                                       values = ["all", "x", "y", "z"],
                                       set_value = "all",
                                       selection_function = self.header_dropdown_selected,
                                       text = "Сектор")
      
   def add_company(self, company):
      
     parser = InvestParser(company)
     
     data = parser.parse()
     
     self.sheet.insert_row([data["country"], data["industry"], data["sector"], data["title"], data["ebitda"], data["net_profit_margin"], data["p_e"], data["p_s"], data["diluted_eps"], data["roe"], data["roa"], data["debt_to_equity"], data["tech_analysis"]])
     
     db_add(data)
      
   def delete_company(self):
      pass
   
   def update_data(self):
      pass
   
   def alalyze_data(self):
      pass
   
   def header_dropdown_selected(self, event = None):
      pass