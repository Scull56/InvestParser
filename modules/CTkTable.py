import customtkinter as ctk
from customtkinter import (
   ThemeManager as tm,
   AppearanceModeTracker as amt
)
from tksheet import Sheet

class CTkTable(Sheet, ctk.CTkBaseClass):
   
   theme_colors = {
      "popup_menu_fg": tm.theme['CTkLabel']['text_color'],
      "popup_menu_bg": tm.theme['CTk']['fg_color'],
      "popup_menu_highlight_bg": tm.theme['DropdownMenu']['hover_color'],
      "popup_menu_highlight_fg": tm.theme['CTkLabel']['text_color'],
      "frame_bg": tm.theme['CTk']['fg_color'],
      "outline_color": tm.theme['CTkFrame']['border_color'],
      "table_grid_fg": tm.theme['CTkFrame']['border_color'],
      "table_bg": tm.theme['CTk']['fg_color'],
      "table_fg": tm.theme['CTkLabel']['text_color'],
      "table_selected_cells_border_fg": tm.theme['CTkLabel']['text_color'],
      "table_selected_cells_bg": tm.theme['DropdownMenu']['hover_color'],
      "table_selected_cells_fg": tm.theme['CTkLabel']['text_color'],
      "table_selected_rows_border_fg": tm.theme['CTkLabel']['text_color'],
      "table_selected_rows_bg": tm.theme['DropdownMenu']['hover_color'],
      "table_selected_rows_fg": tm.theme['CTkLabel']['text_color'],
      "table_selected_columns_border_fg": tm.theme['CTkLabel']['text_color'],
      "table_selected_columns_bg": tm.theme['DropdownMenu']['hover_color'],
      "table_selected_columns_fg": tm.theme['CTkLabel']['text_color'],
      "resizing_line_fg": tm.theme['CTkLabel']['text_color'],
      "drag_and_drop_bg": tm.theme['CTk']['fg_color'],
      "index_bg": tm.theme['CTk']['fg_color'],
      "index_border_fg": tm.theme['CTkFrame']['border_color'],
      "index_grid_fg": tm.theme['CTkFrame']['border_color'],
      "index_fg": tm.theme['CTkLabel']['text_color'],
      "index_selected_cells_bg": tm.theme['DropdownMenu']['hover_color'],
      "index_selected_cells_fg": tm.theme['CTkLabel']['text_color'],
      "index_selected_rows_bg": tm.theme['DropdownMenu']['hover_color'],
      "index_selected_rows_fg": tm.theme['CTkLabel']['text_color'],
      "index_hidden_rows_expander_bg": tm.theme['CTk']['fg_color'],
      "header_bg": tm.theme['CTk']['fg_color'],
      "header_border_fg": tm.theme['CTkFrame']['border_color'],
      "header_grid_fg": tm.theme['CTkFrame']['border_color'],
      "header_fg": tm.theme['CTkLabel']['text_color'],
      "header_selected_cells_bg": tm.theme['DropdownMenu']['hover_color'],
      "header_selected_cells_fg": tm.theme['CTkLabel']['text_color'],
      "header_selected_columns_bg": tm.theme['DropdownMenu']['hover_color'],
      "header_selected_columns_fg": tm.theme['CTkLabel']['text_color'],
      "header_hidden_columns_expander_bg": tm.theme['CTk']['fg_color'],
      "top_left_bg": tm.theme['DropdownMenu']['hover_color'],
      "top_left_fg": tm.theme['DropdownMenu']['hover_color'],
      "top_left_fg_highlight": tm.theme['DropdownMenu']['hover_color'],
   }
   
   def __init__(self, *args, 
                data = [],
                header_align='c',
                header_height="1",
                column_width=120,
                row_height="1",
                align="w",
                **kwargs):
      
      font_family = tm.theme['CTkFont']['family']
      font = (font_family, 13, "normal")
      header_font = (font_family, 13, "bold")
      
      ctk.CTkBaseClass.__init__(self, *args, **kwargs)
      
      Sheet.__init__(self,
                     data=data,
                     header_align=header_align,
                     header_height=header_height,
                     column_width=column_width,
                     row_height=row_height,
                     font=font,
                     index_font=font,
                     header_font=header_font,
                     outline_thickness=1,
                     empty_horizontal=0,
                     empty_vertical=0,
                     align=align,
                     *args, **kwargs)
      
      self.change_theme()
      
   def change_theme(self):
      
      theme = CTkTable.theme_colors.copy()
      
      for key in theme.keys():
         theme[key] = theme[key][amt.appearance_mode]
      
      self.set_options(**theme, redraw=False)
      self.config(bg=theme["table_bg"])
      
      self.MT.recreate_all_selection_boxes()
      self.set_refresh_timer(True)
      
   def config(self, *args, **kwargs):
      Sheet.config(self, **kwargs)
      
   def _draw(self, no_color_updates=False):
      self.change_theme()
      