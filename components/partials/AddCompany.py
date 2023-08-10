import customtkinter as ctk

class AddСompany(ctk.CTkFrame):
   
   def __init__(self, master):
      super().__init__(master)
      
      self.configure(fg_color="transparent", corner_radius=0)
      self.grid(pady=(0, 40), sticky="ew")
      self.grid_columnconfigure((0,1,2,3), weight=1)
      
      label = ctk.CTkLabel(self, text="Добавление новой компании", font=ctk.CTkFont(size=14, weight="bold"))
      label.grid(row=0, column=0, columnspan=5, sticky="w")
      
      sector_input = ctk.CTkComboBox(self, values=("Выбор страны", "Россия", "Китай"))
      sector_input.grid(row=1, column=0, padx=(0, 20), sticky='ew')
      
      sector_input = ctk.CTkComboBox(self, values=("Выбор сектора", "Промышленность", "IT"))
      sector_input.grid(row=1, column=1, padx=(0, 20), sticky='ew')
         
      sub_sector_input = ctk.CTkComboBox(self, values=("Выбор под сектора", "Техника", "Авто"))
      sub_sector_input.grid(row=1, column=2, padx=(0, 20), sticky='ew')
      
      ticker_input = ctk.CTkComboBox(self, values=("Выбор акции", "APPL", "Microsoft"))
      ticker_input.grid(row=1, column=3, padx=(0, 20), sticky='ew')
      
      add_btn = ctk.CTkButton(self, text="Добавить")
      add_btn.grid(row=1, column=4, sticky='ew')