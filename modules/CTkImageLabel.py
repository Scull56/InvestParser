import customtkinter as ctk
from PIL import Image

class CTkImageLabel(ctk.CTkLabel):
   
   def __init__(self, master, light_image_path, dark_image_path, width=None, height=None):
      super().__init__(master, text="")

      light_img = Image.open(light_image_path)
      dark_img = Image.open(dark_image_path)
      
      w = 50
      h = 50
      
      if width != None and height != None:
         w = width
         h = height
         
      elif width != None or height != None:
         
         if width != None:
            w = width
            h = int(width * (light_img.height / light_img.width))
         
         if height != None:
            h = height
            w = int(height * (light_img.width / light_img.height))
      
      img = ctk.CTkImage(
         light_image=light_img, 
         dark_image=dark_img, 
         size=(w, h))
      
      self.configure(image=img)