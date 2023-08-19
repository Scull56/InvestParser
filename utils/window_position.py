def window_center(window, w, h):
   # get screen width and height
   ws = window.winfo_screenwidth() # width of the screen
   hs = window.winfo_screenheight() # height of the screen

   # calculate x and y coordinates for the Tk root window
   x = (ws/2) - (w/2)
   y = (hs/2) - (h/2)

   # set the dimensions of the screen 
   # and where it is placed
   return '%dx%d+%d+%d' % (w, h, x, y)