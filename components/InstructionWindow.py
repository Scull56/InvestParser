import customtkinter as ctk

from modules.CTkText import CTkText
from modules.CTkLink import CTkLink
from modules.CTkImageLabel import CTkImageLabel

from utils.window_position import window_center

class InstructionWindow(ctk.CTkToplevel):
   
   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      
      self.geometry(window_center(self, 400, 500))
      self.title("InvestParser: Инструкция")
      self.resizable(width=False, height=True)
      self.wm_iconbitmap(default='favicon.ico')
      
      self.grid_columnconfigure(0, weight=1)
      self.grid_rowconfigure(0, weight=1)
      
      frame = ctk.CTkScrollableFrame(self, orientation='vertical', fg_color='transparent')
      frame.grid(row=0, column=0, sticky='nsew')
      frame.grid_columnconfigure(0, weight=1)
      frame.grid_rowconfigure(0, weight=1)
      
      body = ctk.CTkFrame(frame, fg_color='transparent')
      body.grid(row=0, column=0, padx=10, pady=10, sticky='ew')
      
      about_text = ''
      
      with open('instructions/about.txt', 'r', encoding="UTF-8") as file:
         about_text = file.read()
      
      ui_text = ''
      
      with open('instructions/ui.txt', 'r', encoding="UTF-8") as file:
         ui_text = file.read()
      
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
      
      message_text = ''
      
      with open('instructions/message.txt', 'r', encoding="UTF-8") as file:
         message_text = file.read()
         
      title_font = ctk.CTkFont(size=16, weight='bold')
      
      about_title = ctk.CTkLabel(body, text='О программе', font=title_font)
      about_title.pack(anchor="w")
      
      about = CTkText(body, text=about_text)
      about.pack(anchor="w", pady=(0, 20))
      
      about_img = CTkImageLabel(
         body,
         light_image_path='instructions/ui_light.png',
         dark_image_path='instructions/ui_dark.png',
         width=360)
      about_img.pack(anchor="w", pady=(0, 10))
      
      about_ui = CTkText(body, text=ui_text)
      about_ui.pack(anchor='w', pady=(0, 20))
      
      link_title = ctk.CTkLabel(body, text='Источник данных', font=title_font)
      link_title.pack(anchor="w")
      
      link = CTkLink(body, 'Investing.com', 'https://www.investing.com/', font_size=12)
      link.pack(anchor="w", pady=(0, 20))
      
      indicators_title = ctk.CTkLabel(body, text='Индикаторы', font=title_font)
      indicators_title.pack(anchor="w")
      
      indicators = CTkText(body, text=indicators_text)
      indicators.pack(anchor="w", pady=(0, 20))
      
      add_title = ctk.CTkLabel(body, text='Добавление компаний', font=title_font)
      add_title.pack(anchor="w")
      
      add_img = CTkImageLabel(
         body,
         light_image_path='instructions/add_light.png',
         dark_image_path='instructions/add_dark.png',
         width=360)
      add_img.pack(anchor="w", pady=(0, 10))
      
      add = CTkText(body, text=add_text)
      add.pack(anchor="w", pady=(0, 20))
      
      delete_title = ctk.CTkLabel(body, text='Удаление компаний', font=title_font)
      delete_title.pack(anchor="w")
      
      delete_img = CTkImageLabel(
         body,
         light_image_path='instructions/delete_light.png',
         dark_image_path='instructions/delete_dark.png',
         width=360)
      delete_img.pack(anchor="w", pady=(0, 10))
      
      delete = CTkText(body, text=delete_text)
      delete.pack(anchor="w", pady=(0, 20))
      
      analyze_title = ctk.CTkLabel(body, text='Анализ', font=title_font)
      analyze_title.pack(anchor="w")
      
      analyze_img = CTkImageLabel(
         body,
         light_image_path='instructions/palete_light.png',
         dark_image_path='instructions/palete_dark.png',
         width=360)
      analyze_img.pack(anchor="w", pady=(0, 10))
      
      analyze = CTkText(body, text=analyze_text)
      analyze.pack(anchor="w", pady=(0, 20))
      
      message_title = ctk.CTkLabel(body, text='Сообщения', font=title_font)
      message_title.pack(anchor="w")
      
      message_img = CTkImageLabel(
         body,
         light_image_path='instructions/message_light.png',
         dark_image_path='instructions/message_dark.png',
         width=360)
      message_img.pack(anchor="w", pady=(0, 10))
      
      message = CTkText(body, text=message_text)
      message.pack(anchor="w")
      
      self.grab_set()