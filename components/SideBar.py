import customtkinter as ctk

from components.partials.AnalyzeOptions import AnalyzeOptions
from components.InstructionWindow import InstructionWindow
class SideBar(ctk.CTkFrame):
   def __init__(self, master):
      super().__init__(master)
      
      self.grid_rowconfigure(0, weight=1)

      body = ctk.CTkFrame(self, fg_color="transparent")
      body.grid(row=0, column=0, padx=20, pady=(20, 40), sticky="nsew")
      body.grid_rowconfigure(1, weight=1)

      # logotype
      logo_label = ctk.CTkLabel(body, text="InvestParser", font=ctk.CTkFont(size=20, weight="bold"))
      logo_label.grid(row=0, column=0)
      
      # Analyzer options
      analyze_options = AnalyzeOptions(body)
      analyze_options.grid(row=1, column=0)

      # Instruction
      instruction_btn = ctk.CTkButton(body, text="Инструкция", command=self.open_instruction)
      instruction_btn.grid(row=6, column=0, sticky="w")

      self.instruction_window = None
      
      # theme select
      theme_mode_label = ctk.CTkLabel(body, text="Цветовая тема:")
      theme_mode_label.grid(row=2, column=0, sticky="w")
      theme_mode_select = ctk.CTkOptionMenu(body, values=["Light", "Dark", "System"],
                                                                     command=self.change_theme_mode_event)
      theme_mode_select.grid(row=3, column=0, sticky="w")

      # scaling select
      scaling_label = ctk.CTkLabel(body, text="Размер интерфейса:")
      scaling_label.grid(row=4, column=0, sticky="w")
      scaling_select = ctk.CTkOptionMenu(body, values=["80%", "90%", "100%", "110%", "120%"],
                                                            command=self.change_scaling_event)
      scaling_select.grid(row=5, column=0, pady=(0, 40), sticky="w")
      
      # set values
      theme_mode_select.set(ctk.get_appearance_mode())
      scaling_select.set(f'{int(ctk.ScalingTracker.widget_scaling * 100)}%')
        
   def change_theme_mode_event(self, new_theme_mode: str):
      ctk.set_appearance_mode(new_theme_mode)

   def change_scaling_event(self, new_scaling: str):
      new_scaling_float = int(new_scaling.replace("%", "")) / 100
      ctk.set_widget_scaling(new_scaling_float)
   
   def open_instruction(self):
      if self.instruction_window is None or not self.instruction_window.winfo_exists():
         self.instruction_window = InstructionWindow()
         self.instruction_window.focus()
      else:
         self.instruction_window.focus()