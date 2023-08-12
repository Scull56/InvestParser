import customtkinter as ctk

import re

from modules.CTkTable import CTkTable

from utils.InvestExceptions import *
from parsers.InvestParser import InvestParser
from analyzers.InvestAnalyzer import InvestAnalyzer

from db.commands import (
   get_companies,
   get_countries,
   get_sectors,
   get_industries,
   add_company as db_add
)



class Table(ctk.CTkFrame):
   
   analyze_colors = {
      "best": "#12ae51",
      "good": "#3f7354",
      "neutral": "#e0ce65",
      "bad": "#8e4141",
      "worst": "#ff1616"
   }
   
   def __init__(self, master):
      super().__init__(master)
      
      self.configure(fg_color="transparent")
      self.grid(sticky="nsew")
      self.grid_rowconfigure(0, weight=1)
      self.grid_columnconfigure(0, weight=1)
      
      ctk.get_appearance_mode()
      
      companies = get_companies()
      countries = get_countries()
      industries = get_industries()
      sectors = get_sectors()
      
      countries = map(lambda item: item[0], countries)
      industries = map(lambda item: item[0], industries)
      sectors = map(lambda item: item[0], sectors)
      
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
                                       values = ["all", *countries],
                                       set_value = "all",
                                       selection_function = self.header_dropdown_selected,
                                       text = "Страна")
      self.sheet.create_header_dropdown(c = 1,
                                       values = ["all", *industries],
                                       set_value = "all",
                                       selection_function = self.header_dropdown_selected,
                                       text = "Индустрия")
      self.sheet.create_header_dropdown(c = 2,
                                       values = ["all", *sectors],
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
      
      sets = {}
      data = self.sheet.data
      
      for i, row in enumerate(data):
         
         group = f"{row[0]}{row[1]}{row[2]}"
         
         if group in sets:
            sets[group].append(i)
            
         else:
            sets[group] = [i]
      
      analyzer = InvestAnalyzer()
      
      for set in sets:
         
         dataSet = [[data[i][4], data[i][5], data[i][6], data[i][7], data[i][8], data[i][9], data[i][10], data[i][11], data[i][12]] for i in set]
         
         dataSet[0] = float(re.split(' ', dataSet[0])[1])
         dataSet[1] = float(re.sub('%', '', dataSet[1]))
         dataSet[2] = float(re.sub('%', '', dataSet[2]))
         dataSet[3] = float(dataSet[3])
         dataSet[4] = float(dataSet[4])
         dataSet[5] = float(dataSet[5])
         dataSet[6] = float(re.sub('%', '', dataSet[6]))
         dataSet[7] = float(re.sub('%', '', dataSet[7]))
         
         analyze_map = analyzer.analyze(set)
         
         analyze_map_colors = [row for row in analyze_map Table.analyze_colors[item] for item in row]
         
         for i, rowIndex in enumerate(set):
            for columnIndex in range(9):
               
               self.sheet.highlight_cells(row=rowIndex, column=columnIndex, bg=analyze_map_colors[i][columnIndex])
         
      self.sheet.redraw()
   
   def header_dropdown_selected(self, event = None):
      
      hdrs = self.sheet.headers()
      hdrs = [hdrs[0], hdrs[1], hdrs[2]]
      
      hdrs[event.column] = event.text
      
      if all(dd == "all" for dd in hdrs):
         self.sheet.display_rows("all")
         
      else:
         rows = [rn for rn, row in enumerate(self.sheet.data) if all(row[c] == e or e == "all" for c, e in enumerate(hdrs))]
         self.sheet.display_rows(rows = rows, all_displayed = False)
         
      self.sheet.redraw()
      
      return float(re.sub('%', '', str))