import customtkinter as ctk

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

      # theme select
      theme_mode_label = ctk.CTkLabel(body, text="Appearance Mode:")
      theme_mode_label.grid(row=2, column=0)
      theme_mode_select = ctk.CTkOptionMenu(body, values=["Light", "Dark", "System"],
                                                                     command=self.change_theme_mode_event)
      theme_mode_select.grid(row=3, column=0)

      # scaling select
      scaling_label = ctk.CTkLabel(body, text="UI Scaling:")
      scaling_label.grid(row=4, column=0)
      scaling_select = ctk.CTkOptionMenu(body, values=["80%", "90%", "100%", "110%", "120%"],
                                                            command=self.change_scaling_event)
      scaling_select.grid(row=5, column=0)
      
      # set default values
      theme_mode_select.set("Dark")
      scaling_select.set("100%")
        
   def change_theme_mode_event(self, new_theme_mode: str):
      ctk.set_appearance_mode(new_theme_mode)

   def change_scaling_event(self, new_scaling: str):
      new_scaling_float = int(new_scaling.replace("%", "")) / 100
      ctk.set_widget_scaling(new_scaling_float)