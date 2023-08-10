import customtkinter as ctk

class ToolBar(ctk.CTkFrame):
   
   def __init__(self, master):
      super().__init__(master)
      
      self.configure(fg_color="transparent")
      self.grid(sticky="e", pady=(0, 20))
      
      update_data_btn = ctk.CTkButton(self, text="Обновить данные")
      update_data_btn.grid(row=0, column=0, padx=(0, 20))
      
      delete_rows_btn = ctk.CTkButton(self, text="Удалить выделенные")
      delete_rows_btn.grid(row=0, column=1)
      
      # radio анализ по сектору и анализ по под сектору