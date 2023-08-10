import customtkinter as ctk

from components.partials.ToolBar import ToolBar
from components.partials.AddCompany import AddСompany
from components.partials.Table import Table

class MainView(ctk.CTkFrame):
   
   def __init__(self, master):
      super().__init__(master)
      
      self.configure(fg_color="transparent", corner_radius=0)
      self.grid_columnconfigure(0, weight=1)
      self.grid_rowconfigure(0, weight=1)
      
      # body
      body = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
      body.grid(column=0, row=0, padx=20, pady=20, sticky="nsew")
      body.grid_columnconfigure(0, weight=1)
      body.grid_rowconfigure(2, weight=1)
      
      # panel for adding new companies
      add_company = AddСompany(body)
      add_company.grid(row=0, column=0)
      
      # tools panel
      toolbar = ToolBar(body)
      toolbar.grid(row=1, column=0)
      
      # table with companies
      table = Table(body)
      table.grid(row=2, column=0)