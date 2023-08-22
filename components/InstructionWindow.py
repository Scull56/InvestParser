import customtkinter as ctk

from modules.CTkText import CTkText

from modules.CTkLink import CTkLink

from utils.window_position import window_center

class InstructionWindow(ctk.CTkToplevel):
   
   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      
      self.geometry(window_center(self, 300, 500))
      self.title("InvestParser: Инструкция")
      self.wm_iconbitmap(default='favicon.ico')
      
      self.grid_columnconfigure(0, weight=1)
      self.grid_rowconfigure(0, weight=1)
      
      frame = ctk.CTkScrollableFrame(self, orientation='vertical', fg_color='transparent')
      frame.grid(row=0, column=0, sticky='nsew')
      frame.grid_columnconfigure(0, weight=1)
      frame.grid_rowconfigure(0, weight=1)
      
      body = ctk.CTkFrame(frame, fg_color='transparent')
      body.grid(row=0, column=0, padx=10, pady=10, sticky='ew')
      body.grid_columnconfigure(0, weight=1)
      
      about_text = ''
      
      with open('instructions/about.txt', 'r', encoding="UTF-8") as file:
         about_text = file.read()
         
      indicators_text = ''
      
      with open('instructions/indicators.txt', 'r', encoding="UTF-8") as file:
         indicators_text = file.read()
         
      add_text = ''
      
      with open('instructions/add_company.txt', 'r', encoding="UTF-8") as file:
         add_text = file.read()
      
      delete_text = ''
      
      with open('instructions/delete_company.txt', 'r', encoding="UTF-8") as file:
         delete_text = file.read()
      
      analyze_text = ''
      
      with open('instructions/analyze.txt', 'r', encoding="UTF-8") as file:
         analyze_text = file.read()
      
      title_font = ctk.CTkFont(size=16, weight='bold')
      
      about_title = ctk.CTkLabel(body, text='О программе', font=title_font)
      about_title.grid(row=0, column=0, sticky='w')
      
      about = CTkText(body, text=about_text, height=80)
      about.grid(row=1, column=0)
      
      link_title = ctk.CTkLabel(body, text='Источник данных', font=title_font)
      link_title.grid(row=2, column=0, sticky='w')
      
      link = CTkLink(body, 'Investing.com', 'https://www.investing.com/', font_size=12)
      link.grid(row=3, column=0, sticky='w')
      
      indicators_title = ctk.CTkLabel(body, text='Индикаторы', font=title_font)
      indicators_title.grid(row=4, column=0, sticky='w')
      
      indicators = CTkText(body, text=indicators_text)
      indicators.grid(row=5, column=0)
      
      add_title = ctk.CTkLabel(body, text='Добавление компаний', font=title_font)
      add_title.grid(row=6, column=0, sticky='w')
      
      add = CTkText(body, text=add_text)
      add.grid(row=7, column=0)
      
      delete_title = ctk.CTkLabel(body, text='Удаление компаний', font=title_font)
      delete_title.grid(row=8, column=0, sticky='w')
      
      delete = CTkText(body, text=delete_text)
      delete.grid(row=9, column=0)
      
      analyze_title = ctk.CTkLabel(body, text='Анализ', font=title_font)
      analyze_title.grid(row=10, column=0, sticky='w')
      
      analyze = CTkText(body, text=analyze_text)
      analyze.grid(row=11, column=0)
      
      self.grab_set()