import customtkinter as ctk
import tksheet as tks

import asyncio
from threading import Thread

from modules.CTkTable import CTkTable

from utils.InvestExceptions import *
from parsers.InvestParser import InvestParser
from analyzers.InvestAnalyzer import InvestAnalyzer

from db.commands import (
   get_companies,
   get_info,
   add_company as db_add,
   delete_companies as db_delete,
   get_last_company_id,
   get_company_by_id,
   get_companies_info,
   update_companies
)

class Table(ctk.CTkFrame):
   
   analyze_colors = {
      "best": ["#54ff9b", "#006128"],
      "good": ["#abffcf", "#20402c"],
      "neutral": ["#fff4b0", "#4f4300"],
      "bad": ["#ffb0b0", "#4f1d1d"],
      "worst": ["#ff9494", "#6e0202"]
   }
   
   def __init__(self, master):
      super().__init__(master)
      
      self.configure(fg_color="transparent")
      self.grid(sticky="nsew")
      self.grid_rowconfigure(0, weight=1)
      self.grid_columnconfigure(0, weight=1)
      
      companies = get_companies()
      info = get_info()
      
      countries = info['country']
      industries = info['industry']
      sectors = info['sector']
      
      self.countries = list(map(lambda item: item[0], countries))
      self.industries = list(map(lambda item: item[0], industries))
      self.sectors = list(map(lambda item: item[0], sectors))
      
      self.analyze = False
      self.analyze_options = [True, True, True]
      self.analyze_sets = None
      self.analyze_definers = None
      
      data = []
      
      for item in companies:
         data.append([item[0], item[3], item[5], item[4], item[6], item[7], item[8], item[9], item[10], item[11], item[12], item[13], item[14], item[15]])
      
      self.sheet = CTkTable(self,
                            data=data,
                            header_align='w',
                            header_height="1",
                            column_width=120,
                            row_height=75)
      
      self.sheet.headers(["ID", "Страна", "Сектор", "Индустрия", "Компания","EBITDA", "Net Profit Margin", "P/E", "P/S", "EPS", "ROE", "ROA", "Debt/Equity", "Технический анализ"])

      self.sheet.hide_columns(columns = 0)
      
      def format_ebitda(value, **kw):
         return f'{round(float(value / 1000000), 2)} млрд.'
      
      self.sheet.format_column(5, formatter_options = tks.formatter(datatypes=[float], format_function = float, to_str_function=format_ebitda))
      
      self.sheet.format_column(6, formatter_options = tks.percentage_formatter(decimals=2))
      self.sheet.format_column(10, formatter_options = tks.percentage_formatter(decimals=2))
      self.sheet.format_column(11, formatter_options = tks.percentage_formatter(decimals=2))
      self.sheet.format_column(12, formatter_options = tks.percentage_formatter(decimals=2))
      
      self.sheet.enable_bindings()
      self.sheet.disable_bindings(['rc_insert_column', 'rc_delete_column', 'edit_cell', 'delete', 'paste',
                                         'cut', 'rc_delete_row', 'rc_insert_row', "edit_index", "edit_header", "drag",
                                         'column_drag_and_drop', "row_drag_and_drop" ])
      
      self.sheet.grid(row=0, column=0, sticky="nsew")
      
      self.sheet.create_header_dropdown(c = 1,
                                       values = ["all", *self.countries],
                                       set_value = "all",
                                       selection_function = self.header_dropdown_selected,
                                       text = "Страна")
      
      self.sheet.create_header_dropdown(c = 2,
                                       values = ["all", *self.sectors],
                                       set_value = "all",
                                       selection_function = self.header_dropdown_selected,
                                       text = "Сектор")
      
      self.sheet.create_header_dropdown(c = 3,
                                       values = ["all", *self.industries],
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
      
      self.update_table()
      
   def delete_company(self):
      
      rows = self.sheet.get_selected_rows(return_tuple=True)
      
      companies_name = []
      rows_id = []
      
      for i in rows:
         companies_name.append(self.sheet.data[i][4])
         rows_id.append(self.sheet.data[i][0])

      db_delete(rows_id)
      
      self.sheet.delete_rows(rows)
      
      self.update_table()
      
      return companies_name
   
   def update_table(self):
      
      if self.analyze:
         self.analyze_data(*self.analyze_options)
         
      info = get_info()
         
      countries = info['country']
      industries = info['industry']
      sectors = info['sector']
      
      countries = list(map(lambda item: item[0], countries))
      industries = list(map(lambda item: item[0], industries))
      sectors = list(map(lambda item: item[0], sectors))
      
      if (len(self.countries) != len(countries)):
         
         self.countries = countries
         self.sheet.set_header_dropdown_values(c=1, values=['all', *self.countries])
         
      if (len(self.sectors) != len(sectors)):
         
         self.sectors = sectors
         self.sheet.set_header_dropdown_values(c=2, values=['all', *self.sectors])
         
      if (len(self.industries) != len(industries)):
         
         self.industries = industries
         self.sheet.set_header_dropdown_values(c=3, values=['all', *self.industries])
         
   def update_data(self, callback):
      
      url_info = get_companies_info()
      
      if len(url_info) == 0:
         raise NotHaveDataForUpdate()
      
      asyncio.set_event_loop
      
      def update_ui(companies):
         
         data = []
               
         for item in companies:
            data.append([item[0], item[3], item[5], item[4], item[6], item[7], item[8], item[9], item[10], item[11], item[12], item[13], item[14], item[15]])
         
         self.sheet.set_sheet_data(data=data)
         
         self.update_table()
      
      def update_thread():
         
         data_list = []
         errors = {
            'not_found': [],
            'not_params': []
         }
         
         for info in url_info:
            
            parser = InvestParser(info[1], info[2])
            
            data = None
            
            try:
               data = parser.parse()
               data['id'] = info[0]
               data_list.append(data)
               
            except NotFoundParams as error:
               errors['not_params'].append((info[3], error.params))
               
            except NotFoundCompany:
               errors['not_found'].append(info[3])
            
            except Exception as exc:
               raise exc()

         async def db_update():
            await update_companies(data_list)
         
         asyncio.run(db_update())
         
         companies = get_companies()
         
         update_ui(companies)
         callback(errors)

      thread = Thread(target=update_thread)
      thread.start()
   
   def set_scale(self, value):
      
      self.sheet.set_scale(value)
   
   def analyze_data(self, country, sector, industry):
      
      self.analyze = True
      self.analyze_options = [country, sector, industry]
      
      sets = {}
      data = self.sheet.data
      
      if len(data) == 0:
         return
      
      if country or sector or industry:
      
         for i, row in enumerate(data):
            
            group = ''
            
            if country: group += row[1]
            if sector: group += row[2]
            if industry: group += row[3]
            
            if group in sets:
               sets[group].append(i)
               
            else:
               sets[group] = [i]
      else:
         
         sets = {'all': range(len(data))}
      
      analyzer = InvestAnalyzer(["more", "more", "near_zero", "near_zero", "more", "more", "more", "less", "value"])
      
      self.analyze_sets = sets
      
      definers = {}
      
      for set in sets:
         
         dataSet = []
         
         for rowIndex in sets[set]:
            
            dataSet.append(data[rowIndex][5:14])
         
         analyze_map = analyzer.analyze(dataSet)
         
         definers[set] = analyze_map
      
      self.analyze_definers = definers
      
      self.highlight_table()
   
   def de_analyze_data(self):
      
      self.analyze = False
      
      self.sheet.dehighlight_all()
   
   def highlight_table(self):
      
      self.sheet.dehighlight_all()
      
      theme_index = ctk.AppearanceModeTracker.appearance_mode
      
      sets = self.analyze_sets
      maps = self.analyze_definers
      
      for set in sets:
         for i in range(len(maps[set])):
            for j in range(len(maps[set][i])):
               
               bg = Table.analyze_colors[maps[set][i][j]][theme_index]
               rowIndex = sets[set][i]
               
               self.sheet.highlight_cells(row=rowIndex, column= 5 + j, bg=bg)
               
      self.sheet.redraw()
   
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
   
   def _draw(self, no_color_updates=False):
      super()._draw(no_color_updates=no_color_updates)
      
      if hasattr(self, 'sheet') and self.analyze:

         self.highlight_table()