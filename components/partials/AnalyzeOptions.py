import customtkinter as ctk
from utils.storage import storage


class AnalyzeOptions(ctk.CTkFrame):
   
   def __init__(self, master):
      
      super().__init__(master)
      
      self.grid(sticky='w')
      
      self.switcher = ctk.CTkSwitch(self, text="Анализ", command=self.switch)
      self.switcher.grid(row=0, column=0, sticky="w")
      
      self.label = ctk.CTkLabel(self, text="Учитывать:")
      self.label.grid(row=1, column=0, sticky="w")
      
      self.country = ctk.CTkCheckBox(self, text="Страна", command=self.update_options)
      self.country.grid(row=2, column=0, pady=(0, 5), sticky="w")
      self.country.select()
      
      self.sector = ctk.CTkCheckBox(self, text="Сектор", command=self.update_options)
      self.sector.grid(row=3, column=0, pady=(0, 5),sticky="w")
      self.sector.select()
      
      self.industry = ctk.CTkCheckBox(self, text="Индустрия", command=self.update_options)
      self.industry.grid(row=4, column=0, sticky="w")
      self.industry.select()
      
   def update_options(self):
      
      self.switch()
   
   def switch(self):
      
      table = storage['table']
      
      if table != None:
      
         if self.switcher.get():
            
            table.analyze_data(self.country.get(), self.sector.get(), self.industry.get())
            
         else:
            table.de_analyze_data()