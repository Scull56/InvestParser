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
   delete_companies as db_delete,
   get_last_company_id,
   get_company_by_id
)

class Table(ctk.CTkFrame):
   
   analyze_colors = {
      "best": "#084722",
      "good": "#01240f",
      "neutral": "#453b00",
      "bad": "#4a0101",
      "worst": "#6e0202"
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
         data.append([item[0], item[3], item[5], item[4], item[6], item[7], item[8], item[9], item[10], item[11], item[12], item[13], item[14], item[15]])
      
      self.sheet = CTkTable(self,
                            data=data,
                            header_align='w',
                            header_height="1",
                            column_width=120,
                            row_height=75)
      
      self.sheet.headers(["ID", "Страна","Сектор", "Индустрия", "Компания","EBITDA", "Net Profit Margin %", "P/E", "P/S", "EPS", "ROE %", "ROA %", "Debt/Equity %", "Технический анализ"])

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
                                       values = ["all", *sectors],
                                       set_value = "all",
                                       selection_function = self.header_dropdown_selected,
                                       text = "Сектор")
      
      self.sheet.create_header_dropdown(c = 3,
                                       values = ["all", *industries],
                                       set_value = "all",
                                       selection_function = self.header_dropdown_selected,
                                       text = "Индустрия")
      
   def add_company(self, id, url):
      
      check = get_company_by_id(id)
      
      if len(check) > 0:
         raise CompanyAlreadyAdded()
      
      parser = InvestParser(id, url)
      
      data = parser.parse()
      
      data['url'] = url
      data['company_id'] = id
      
      db_add(data)
      
      lastId = get_last_company_id()
      
      lastId = lastId[0][0]
      
      self.sheet.insert_row([lastId, data["country"], data["sector"], data["industry"], data["title"], data["ebitda"], data["net_profit_margin"], data["p_e"], data["p_s"], data["eps"], data["roe"], data["roa"], data["debt_to_equity"], data["tech_analysis"]])
      
      self.analyze_data()
      
   def delete_company(self):
      rows = self.sheet.get_selected_rows()
      
      rows_id = map(lambda i: self.sheet.data[i][0], rows)
      
      db_delete(rows_id)
      
      self.sheet.delete_rows(rows)
      
      self.analyze_data()
   
   def update_data(self):
      pass
   
   def set_scale(self):
      pass
   
   def analyze_data(self, country, sector, industry):
      
      sets = {}
      data = self.sheet.data
      
      if len(data) == 0:
         return
         
      for i, row in enumerate(data):
         
         group = ''
         
         if country: group += row[1]
         if sector: group += row[2]
         if industry: group += row[3]
         
         if group in sets:
            sets[group].append(i)
            
         else:
            sets[group] = [i]
      
      analyzer = InvestAnalyzer(["more", "more", "near_zero", "near_zero", "more", "more", "more", "less", "value"])
      
      for set in sets:
         
         dataSet = []
         
         for rowIndex in sets[set]:
            
            dataSet.append(data[rowIndex][5:14])
         
         analyze_map = analyzer.analyze(dataSet)
         
         for i in range(len(analyze_map)):
            for j in range(len(analyze_map[i])):
               
               bg = Table.analyze_colors[analyze_map[i][j]]
               rowIndex = sets[set][i]
               
               self.sheet.highlight_cells(row=rowIndex, column= 5 + j, bg=bg)
               
      self.sheet.redraw()
   
   def de_analyze_data(self):
      
      self.sheet.dehighlight_all()
   
   def header_dropdown_selected(self, event = None):
      
      hdrs = self.sheet.headers()
      
      hdrs = [hdrs[1], hdrs[2], hdrs[3]]
      hdrs[event.column] = event.text
      
      if all(dd == "all" for dd in hdrs):
         self.sheet.display_rows("all")
         
      else:
         
         rows = [rn for rn, row in enumerate(self.sheet.data) if all(row[c + 1] == e or e == "all" for c, e in enumerate(hdrs))]
         self.sheet.display_rows(rows = rows, all_displayed = False)
         
      self.sheet.redraw()