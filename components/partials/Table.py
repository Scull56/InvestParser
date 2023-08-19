import customtkinter as ctk
import tksheet

from modules.CTkTable import CTkTable

from utils.InvestExceptions import *
from parsers.InvestParser import InvestParser
from analyzers.InvestAnalyzer import InvestAnalyzer

from db.commands import (
   get_companies,
   get_countries,
   get_sectors,
   get_industries,
   add_company as db_add,
   delete_companies as db_delete
)

class Table(ctk.CTkFrame):
   
   analyze_colors = {
      "best": "#0d7a39",
      "good": "#00451c",
      "neutral": "#7d7338",
      "bad": "#570000",
      "worst": "#910404"
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
         data.append([item[0], item[3], item[4], item[5], item[6], item[7], item[8], item[9], item[10], item[11], item[12], item[13], item[14], item[15]])
      
      self.sheet = CTkTable(self,
                            data=data,
                            header_align='w',
                            header_height="1",
                            column_width=120,
                            row_height=75)
      
      self.sheet.headers(["ID", "Страна","Индустрия","Сектор","Компания","EBITDA", "Net Profit Margin %", "P/E", "P/S", "EPS", "ROE %", "ROA %", "Debt/Equity %", "Технический анализ"])

      self.sheet.hide_columns(columns = 0)
      
      self.sheet.enable_bindings()
      self.sheet.disable_bindings(['rc_insert_column', 'rc_delete_column', 'edit_cell', 'delete', 'paste',
                                         'cut', 'rc_delete_row', 'rc_insert_row', "edit_index", "edit_header", "drag",
                                         'column_drag_and_drop', "row_drag_and_drop" ])
      
      self.sheet.grid(row=0, column=0, sticky="nsew")
      
      self.sheet.create_header_dropdown(c = 1,
                                       values = ["all", *countries],
                                       set_value = "all",
                                       selection_function = self.header_dropdown_selected,
                                       text = "Страна")
      self.sheet.create_header_dropdown(c = 2,
                                       values = ["all", *industries],
                                       set_value = "all",
                                       selection_function = self.header_dropdown_selected,
                                       text = "Индустрия")
      self.sheet.create_header_dropdown(c = 3,
                                       values = ["all", *sectors],
                                       set_value = "all",
                                       selection_function = self.header_dropdown_selected,
                                       text = "Сектор")
      self.analyze_data()
      
   def add_company(self, id, url):
      
      parser = InvestParser(id, url)
      
      data = parser.parse()
      
      newId = self.sheet.data[-1][0] + 1
      
      self.sheet.insert_row([newId, data["country"], data["industry"], data["sector"], data["title"], data["ebitda"], data["net_profit_margin"], data["p_e"], data["p_s"], data["eps"], data["roe"], data["roa"], data["debt_to_equity"], data["tech_analysis"]])
      
      data['url'] = url
      data['company_id'] = id
      
      db_add(data)
      
      self.analyze_data()
      
   def delete_company(self):
      rows = self.sheet.get_selected_rows()
      
      rows_id = map(lambda i: self.sheet.data[i][0], rows)
      
      db_delete(rows_id)
      
      self.sheet.delete_rows(rows)
   
   def update_data(self):
      pass
   
   def analyze_data(self):
      
      sets = {}
      data = self.sheet.data
      
      for i, row in enumerate(data):
         
         group = f"{row[1]}{row[2]}{row[3]}"
         
         if group in sets:
            sets[group].append(i)
            
         else:
            sets[group] = [i]
      
      analyzer = InvestAnalyzer()
      
      for set in sets:
         
         dataSet = []
         
         for item in sets[set]:
            
            dataSet.append([
               data[item][5], 
               data[item][6], 
               data[item][7], 
               data[item][8], 
               data[item][9], 
               data[item][10], 
               data[item][11], 
               data[item][12], 
               data[item][13]
            ])
         
         print(dataSet)
         
         analyze_map = analyzer.analyze(dataSet)
         
         for i in range(len(analyze_map)):
            for j in range(len(analyze_map[i])):
               analyze_map[i][j] = Table.analyze_colors[analyze_map[i][j]]
         
            for rowIndex in sets[set]:
               for columnIndex in range(9):
                  
                  self.sheet.highlight_cells(row=rowIndex, column= 5 + columnIndex, fg="white", bg=analyze_map[i][columnIndex])

      self.sheet.redraw()
   
   def header_dropdown_selected(self, event = None):
      
      hdrs = self.sheet.headers()
      hdrs = [hdrs[1], hdrs[2], hdrs[3]]
      
      hdrs[event.column] = event.text
      
      if all(dd == "all" for dd in hdrs):
         self.sheet.display_rows("all")
         
      else:
         rows = [rn for rn, row in enumerate(self.sheet.data) if all(row[c] == e or e == "all" for c, e in enumerate(hdrs))]
         self.sheet.display_rows(rows = rows, all_displayed = False)
         
      self.sheet.redraw()