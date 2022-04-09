from tkinter import *
import tkinter as tk
from geopy.geocoders import Nominatim
from tkinter import ttk, messagebox

from urllib.request import urlopen
from PIL import Image, ImageTk

root=Tk()
root.title("Weather App")
root.geometry("900x500+300+200")
root.resizable(False, False)

def get_image(icon):
    print(icon)
    
    try:
        # from openweathermap.org
        #URL = "https://openweathermap.org/img/w/"+icon+".png"      # small icons
        #URL = "https://openweathermap.org/img/wn/"+icon+"@2x.png"  # big icons
        
        # from github
        URL = "https://raw.githubusercontent.com/jdavid54/tkinter/main/Weather%20App/weather_icons/"+icon+"@2x.png" 
        print(URL)
        u = urlopen(URL)
        raw_data = u.read()
        u.close()
        
        # read from local file
#         file = 'weather_icons/'+icon+'@2x.png'
#         with open(file,'rb') as f:
#             raw_data = f.read()
                    
        photo = ImageTk.PhotoImage(data=raw_data) # <-----

        label = tk.Label(image=photo)
        label.image = photo
        label.config(bg="lightgrey")
        label.place(x=700, y=150)
    except Exception as e:
        messagebox.showerror("Weather App","No weather icon found !!")

icon = '11d'
get_image(icon)
root.mainloop()