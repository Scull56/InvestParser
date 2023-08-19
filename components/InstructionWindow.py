import customtkinter as ctk

from utils.window_position import window_center

class InstructionWindow(ctk.CTkToplevel):
   
   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      
      self.grid_columnconfigure(0, weight=1)
      self.grid_rowconfigure(0, weight=1)
      
      frame = ctk.CTkScrollableFrame(self, orientation='vertical')
      frame.grid(row=0, column=0, sticky='nsew')
      
      text = None
      
      with open('instructions/instruction.txt', 'r', encoding="UTF-8") as file:
         text = file.read()
      
      text_box = ctk.CTkTextbox(frame)
      text_box.insert('0.0', text)
      text_box.configure(state="disabled")
      text_box.grid(row=0, column=0, sticky="ew")
      
      self.geometry(window_center(self, 300, 500))
      self.title("InvestParser: Инструкция")
      
      self.grab_set()