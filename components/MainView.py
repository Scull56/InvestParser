import customtkinter as ctk

from components.partials.ToolBar import ToolBar
from components.partials.AddCompany import AddСompany
from components.partials.Table import Table
from components.partials.Message import Message

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
      
      # table with companies
      table = Table(body)
      table.grid(row=2, column=0, columnspan=2)
      
      # label for show error mesages
      status_label = Message(body)
      status_label.grid(row=1, column=0, padx=(0, 20), pady=(0, 20))
      
      # panel for adding new companies
      add_company = AddСompany(body, table, status_label)
      add_company.grid(row=0, column=0, pady=(0, 40), columnspan=2)

      # tools panel
      toolbar = ToolBar(body, table, status_label)
      toolbar.grid(row=1, column=1, pady=(0, 20))